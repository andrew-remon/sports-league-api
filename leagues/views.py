from django.shortcuts import render
from django.http import JsonResponse, Http404
from leagues.models import Team, League, Player
from django.views.decorators.csrf import csrf_exempt
from leagues.serializers import LeagueSerializer
from rest_framework.generics import ListCreateAPIView
import json

# Create your views here.
@csrf_exempt # we use this decorator to bypass the csrf so Django could perform POST methods
def league_collection_view(request):
    if request.method == "GET":
        leagues = League.objects.all()
        leagues_list = []

        for league in leagues:
            leagues_list.append({"id": league.id, "name": league.name, "description": league.description, "max_teams": league.max_teams, "created_at": league.created_at})

        return JsonResponse(leagues_list, safe=False)

    elif request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid or malformed JSON"}, status=400)

        # validation checks
        if not isinstance(body, dict):
            return JsonResponse({"error": "Request body must be a JSON object"}, status=400)

        if "name" in body:
            if not isinstance(body["name"], str) or not body["name"].strip():
                return JsonResponse({"error":"name is required and must be non-emtpy string"}, status=400)

        if "max_teams" in body:
            if not isinstance(body["max_teams"],int):
                return JsonResponse({"error":"max_teams must be int"}, status=400)
            if body["max_teams"] <= 0:
                return JsonResponse({"error":"max_teams must be > 0"}, status=400)

        # Validation passed, create the new_league record
        new_league = League.objects.create(name=body["name"], description=body.get("description", ""), max_teams = body.get("max_teams", 20),)
        return JsonResponse(
            {
                "id":new_league.id,
                "name":new_league.name,
                "max_teams":new_league.max_teams
            },
            status=201)

    # what if other request method get called (e.g PUT)
    return JsonResponse({"error":"Unsupported Method"}, status=405)

def retrieve_league_by_id(request, league_id):
    if request.method != "GET":
       return JsonResponse({"error":"Unsupported Method"}, status=405)

    try:
        league = League.objects.get(pk=league_id)
    except League.DoesNotExist:
        raise JsonResponse({"error":"League Not Found"}, status=404)
    else:
        return JsonResponse({"id": league.id, "name": league.name, "description": league.description, "max_teams": league.max_teams, "created_at": league.created_at})

def team_collection_view(request, league_id):
    if request.method != "GET":
        return JsonResponse({"error":"Unsupported Method"}, status=405)

    try:
        league = League.objects.get(pk=league_id)
    except League.DoesNotExist:
        raise JsonResponse({"error":"League Not Found"}, status=404)
    else:
            teams = Team.objects.filter(league=league)
            teams_list = []

            for team in teams:
                teams_list.append({"id": team.id, "name": team.name})

            return JsonResponse(teams_list, safe=False)

class LeagueListCreateAPIView(ListCreateAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
