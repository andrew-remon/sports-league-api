# third-party
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
import pytest

from leagues.models import Match, MatchResult

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
def test_record_result_conflict(api_client, sample_league, sample_team, sample_match):

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
