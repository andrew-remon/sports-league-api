from django.shortcuts import render
from django.http import JsonResponse, Http404
from leagues.models import Team, League, Player
from leagues.services import get_standings
from django.views.decorators.csrf import csrf_exempt
from leagues.serializers import *
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
import json

# ------------- Old Representation - Django Views Functions --------------------
# @csrf_exempt # we use this decorator to bypass the csrf so Django could perform POST methods
# def league_collection_view(request):
#     if request.method == "GET":
#         leagues = League.objects.all()
#         leagues_list = []

#         for league in leagues:
#             leagues_list.append({"id": league.id, "name": league.name, "description": league.description, "max_teams": league.max_teams, "created_at": league.created_at})

#         return JsonResponse(leagues_list, safe=False)

#     elif request.method == "POST":
#         try:
#             body = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid or malformed JSON"}, status=400)

#         # validation checks
#         if not isinstance(body, dict):
#             return JsonResponse({"error": "Request body must be a JSON object"}, status=400)

#         if "name" in body:
#             if not isinstance(body["name"], str) or not body["name"].strip():
#                 return JsonResponse({"error":"name is required and must be non-emtpy string"}, status=400)

#         if "max_teams" in body:
#             if not isinstance(body["max_teams"],int):
#                 return JsonResponse({"error":"max_teams must be int"}, status=400)
#             if body["max_teams"] <= 0:
#                 return JsonResponse({"error":"max_teams must be > 0"}, status=400)

#         # Validation passed, create the new_league record
#         new_league = League.objects.create(name=body["name"], description=body.get("description", ""), max_teams = body.get("max_teams", 20),)
#         return JsonResponse(
#             {
#                 "id":new_league.id,
#                 "name":new_league.name,
#                 "max_teams":new_league.max_teams
#             },
#             status=201)

#     # what if other request method get called (e.g PUT)
#     return JsonResponse({"error":"Unsupported Method"}, status=405)

# def retrieve_league_by_id(request, league_id):
#     if request.method != "GET":
#        return JsonResponse({"error":"Unsupported Method"}, status=405)

#     try:
#         league = League.objects.get(pk=league_id)
#     except League.DoesNotExist:
#         raise JsonResponse({"error":"League Not Found"}, status=404)
#     else:
#         return JsonResponse({"id": league.id, "name": league.name, "description": league.description, "max_teams": league.max_teams, "created_at": league.created_at})

# def team_collection_view(request, league_id):
#     if request.method != "GET":
#         return JsonResponse({"error":"Unsupported Method"}, status=405)

#     try:
#         league = League.objects.get(pk=league_id)
#     except League.DoesNotExist:
#         raise JsonResponse({"error":"League Not Found"}, status=404)
#     else:
#             teams = Team.objects.filter(league=league)
#             teams_list = []

#             for team in teams:
#                 teams_list.append({"id": team.id, "name": team.name})

#             return JsonResponse(teams_list, safe=False)

# Using Generic Class View
# class LeagueListCreateAPIView(ListCreateAPIView):
#     queryset = League.objects.all()
#     serializer_class = LeagueSerializer
# =============================================================

# Create your views here.
class LeagueViewSet(ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

    @action(detail=True, methods=['get'])
    def standings(self, request, pk=None):
        standings = get_standings(pk)
        serializer = StandingsSerializer(standings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        league_id = self.request.query_params.get("league")
        if league_id:
            queryset = queryset.filter(league__id=league_id)
        return queryset.select_related("league").prefetch_related("players")

    @action(detail=True, methods=['get'])
    def players(self, request, pk=None):
        players = Player.objects.filter(team__pk=pk).select_related("team__league")
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        team_id = self.request.query_params.get("team")
        position = self.request.query_params.get("position")
        if team_id:
            queryset= queryset.filter(team__id=team_id)
        if position:
            queryset= queryset.filter(position=position)
        return queryset.select_related("team__league")

class MatchViewSet(ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        league_id = self.request.query_params.get("league")
        status = self.request.query_params.get("status")
        if league_id:
            queryset = queryset.filter(league__id = league_id)
        if status:
            queryset = queryset.filter(status = status)
        return queryset.select_related("league", "home_team", "away_tam", "result")

    @action(detail=True, methods=['post'])
    def record_result(self, request, pk=None):
        match = self.get_object()
        result = MatchResult.objects.create(
            match= match,
            home_score=request.data["home_score"],
            away_score=request.data["away_score"],
            )
        match.status = Match.MatchStatus.COMPLETED
        match.save()

        serializer = MatchResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
