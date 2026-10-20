# third-party
import pytest
from django.urls import reverse
from rest_framework import status
from utils.exceptions import ValidationError

from leagues.models import Match, MatchResult
from leagues.serializers import LeagueSerializer, TeamDetailSerializer, MatchSerializer, StandingsSerializer
from tests.factories import LeagueFactory, MatchFactory, TeamFactory

@pytest.mark.django_db
def test_create_match_with_result(api_client, sample_league, sample_team):

    league = sample_league(name="Premier League", max_teams=20)

    team_a = sample_team(name="Leeds United", league=league, city="Leeds")
    team_b = sample_team(name="Liverpool", league=league, city="Liverpool")

    data = {
         "league": league.id, "home_team": team_b.id, "away_team": team_a.id,
         "match_day": 28, "scheduled_date": "2026-07-15T18:00:00Z",
         "result": {"home_score": 5, "away_score": 1}}

    url = reverse("match-list")
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    results = response.data["result"]
    assert response.data["result"]["home_score"] == data["result"]["home_score"]
    assert response.data["result"]["away_score"] == data["result"]["away_score"]
    assert response.data["home_team"] == data["home_team"]

@pytest.mark.django_db
def test_record_result_conflict(api_client, sample_league, sample_team, sample_match, admin_user):
    api_client.force_authenticate(user=admin_user)
    league = sample_league(name="Premier League", max_teams=20)

    team_a = sample_team(name="Leeds United", league=league, city="Leeds")
    team_b = sample_team(name="Liverpool", league=league, city="Liverpool")

    m1 = sample_match(
        league=league,
        home_team=team_b,
        away_team=team_a,
        match_day=28,
        status=Match.MatchStatus.COMPLETED,
    )

    MatchResult.objects.create(
        home_score = 5,
        away_score = 3,
        match = m1,
    )

    data = {"home_score": 5, "away_score": 1, "match": m1.id}

    url = reverse("match-record-result", kwargs={"pk": m1.id})
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_409_CONFLICT

@pytest.mark.django_db
def test_create_match_without_result(api_client, sample_league, sample_team):

    league = sample_league(name="Premier League", max_teams=20)

    team_a = sample_team(name="Fulham", league=league, city="London")
    team_b = sample_team(name="Liverpool", league=league, city="Liverpool")

    data = {
         "league": league.id, "home_team": team_b.id, "away_team": team_a.id,
         "match_day": 27, "scheduled_date": "2026-07-15T18:00:00Z"}

    url = reverse("match-list")
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    results = response.data["result"]
    assert response.data["home_team"] == data["home_team"]
    assert response.data['status'] == "scheduled"


@pytest.mark.django_db
def test_league_serializer_valid():
    data = {"name": "Premier League"}
    serializer = LeagueSerializer(data=data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_league_serializer_empty_name():
    data = {"name": ""}
    serializer = LeagueSerializer(data=data)
    assert serializer.is_valid() == False

@pytest.mark.django_db
def test_team_serializer_read_nests_league():
    league = LeagueFactory.create()
    team = TeamFactory.create(league=league)
    serializer = TeamDetailSerializer(team)
    assert isinstance(serializer.data["league"], dict)
    assert serializer.data["league"]["id"] == league.id
    assert serializer.data["league"]["name"] == league.name

@pytest.mark.django_db
def test_team_serializer_write_accepts_pk():
    league = LeagueFactory.create()
    team_data = {
        "name":"Man City",
        "city":"Manchester",
        "league":league.id
    }
    serializer = TeamDetailSerializer(data=team_data)
    assert serializer.is_valid()
    assert serializer.validated_data.get("league") == league

@pytest.mark.django_db
def test_match_serializer_validation_same_teams():
    team = TeamFactory.create()
    match_data = {
        "home_team":team.id,
        "away_team":team.id,
        "league":5
    }
    serializer = MatchSerializer(data = match_data)
    assert serializer.is_valid() == False

def test_standings_serializer_output():
    standings_data = {
        "team_name":"Man City",
        "played":10,
        "won":7,
        "drawn":2,
        "lost":1,
        "goals_for":23,
        "goals_against":11,
        "goal_difference":12,
        "points":23
    }

    serializer = StandingsSerializer(standings_data)
    assert serializer.data["team_name"] == "Man City"
    assert set(serializer.data.keys()) == {"team_name", "played", "won", "drawn", "lost", "goals_for", "goals_against", "goal_difference", "points"}
