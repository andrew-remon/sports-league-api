# third-party
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

# local
from leagues.models import Team, League, Player, Match
from leagues.services import get_standings
from leagues.filters import TeamFilter, PlayerFilter, MatchFilter
from leagues.serializers import LeagueSerializer, MatchSerializer, TeamSerializer, PlayerSerializer, MatchResultSerializer, StandingsSerializer

# import json
# from django.shortcuts import render
# from django.http import JsonResponse, Http404
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.generics import ListCreateAPIView
# from rest_framework.renderers import JSONRenderer

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
    ordering_fields = ['name', 'created_at']
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'standings':
            return StandingsSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="Create standings table for a specific league.",
        description="Calculates every team record stats, then serializes each record by StandingsSerializer and creates the standings table.",
        responses={
            200: StandingsSerializer(many=True),
            404: OpenApiResponse(description="League ID not found")
        }
    )
    @action(detail=True, methods=['get'])
    def standings(self, request, pk=None):
        standings = get_standings(pk)
        serializer = self.get_serializer(standings, many=True) # many=true returns a ListSerializer
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_class = TeamFilter
    ordering_fields = ['name', 'founded_year']
    search_fields = ['name', 'city']

    def get_queryset(self):
        queryset = super().get_queryset() # Team.objects.all()
        league_id = self.request.query_params.get("league")
        if league_id:
            queryset = queryset.filter(league__id=league_id)
        return queryset.select_related("league").prefetch_related("players")

    def get_serializer_class(self):
        if self.action == 'players':
            return PlayerSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="Show all players of a specific team",
        description="Filters from players table with the specific team ID, then shows each player record",
        responses= {
            200: PlayerSerializer(many=True),
            404: OpenApiResponse(description="Team ID not found")
        }
    )
    @action(detail=True, methods=['get'])
    def players(self, request, pk=None):
        players = Player.objects.filter(team__pk=pk).select_related("team__league")
        # we use get_serializer method to preserve the context(request, formal, view)
        serializer = self.get_serializer(players, many=True) # was: PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filterset_class = PlayerFilter
    ordering_fields = ['last_name', 'jersey_number']
    search_fields = ['first_name', 'last_name']

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
    filterset_class = MatchFilter
    ordering_fields = ['scheduled_date', 'match_day']
    search_fields = ['home_team__name', 'away_team__name']

    def get_queryset(self):
        queryset = super().get_queryset() # refers to Match.objects.all()
        league_id = self.request.query_params.get("league")
        # match_status = self.request.query_params.get("match_status")
        if league_id:
            queryset = queryset.filter(league__id = league_id)
        # if match_status:
        #     queryset = queryset.filter(status = match_status)

        # return queryset.select_related("league", "home_team", "away_team", "result")

        return queryset.select_related("result") # other fields are only used by their pk (which is inside the match row in DB, no JOIN needed)

    @extend_schema(
        summary="Record Match Score Result",
        description="Submits the final score for a scheduled match. This marks the match status as COMPLETED and creates the associated MatchResult record.",
        request=MatchResultSerializer,
        responses={
            201: MatchResultSerializer,
            400: OpenApiResponse(description="Invalid request payload (e.g, negative scores, invalid match ID)"),
            404: OpenApiResponse(description="Match Not Found")
        }
    )
    @action(detail=True, methods=['post'])
    def record_result(self, request, pk=None):
        match = self.get_object()
        serializer = MatchResultSerializer(data=request.data) # deserialization
        serializer.is_valid(raise_exception=True)
        # first match: refer to the field in MatchResultSerializer, should be the same name, as this will be the kwarg key before saving.
        # second match: the match variable in this method
        serializer.save(match=match)
        match.status = Match.MatchStatus.COMPLETED
        match.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) # serialization

