# third-party
from django.urls import reverse
from rest_framework import status
import pytest

# local
from leagues.models import Match, MatchResult


@pytest.mark.django_db
def test_standings_empty_league(api_client, sample_league):
    created_league = sample_league(name="Premier League", max_teams=20)

    url = reverse("league-standings", kwargs={"pk": created_league.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) == 0


@pytest.mark.django_db
def test_standings_with_results(api_client, sample_league, sample_team):
    league = sample_league(name="Premier League", max_teams=20)

    mancity = sample_team(name="Manchester City", league=league, city="Manchester")
    arsenal = sample_team(name="Arsenal", league=league, city="London")
    chelsea = sample_team(name="Chelsea", league=league, city="London")
    liverpool = sample_team(name="Liverpool", league=league, city="Liverpool")

    m1 = Match.objects.create(
        league=league,
        home_team=mancity,
        away_team=liverpool,
        match_day=5,
        status=Match.MatchStatus.SCHEDULED,
    )
    m2 = Match.objects.create(
        league=league,
        home_team=mancity,
        away_team=arsenal,
        match_day=6,
        status=Match.MatchStatus.SCHEDULED,
    )
    m3 = Match.objects.create(
        league=league,
        home_team=chelsea,
        away_team=liverpool,
        match_day=11,
        status=Match.MatchStatus.SCHEDULED,
    )
    m4 = Match.objects.create(
        league=league,
        home_team=arsenal,
        away_team=chelsea,
        match_day=3,
        status=Match.MatchStatus.SCHEDULED,
    )

    MatchResult.objects.create(
        match=m1,
        home_score=3,
        away_score=1,
    )
    MatchResult.objects.create(
        match=m2,
        home_score=4,
        away_score=2,
    )
    MatchResult.objects.create(
        match=m3,
        home_score=1,
        away_score=2,
    )
    MatchResult.objects.create(
        match=m4,
        home_score=3,
        away_score=0,
    )

    m1.status = Match.MatchStatus.COMPLETED
    m1.save()
    m2.status = Match.MatchStatus.COMPLETED
    m2.save()
    m3.status = Match.MatchStatus.COMPLETED
    m3.save()
    m4.status = Match.MatchStatus.COMPLETED
    m4.save()

    url = reverse("league-standings", kwargs={"pk": league.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) == 4
    assert response.data[0]["team_name"] == mancity.name
    assert response.data[0]["played"] == 2
    assert response.data[0]["won"] == 2
    assert response.data[0]["drawn"] == 0
    assert response.data[0]["lost"] == 0
    assert response.data[0]["goals_for"] == 7
    assert response.data[0]["goals_against"] == 3
    assert response.data[0]["points"] == 6
    assert response.data[3]["team_name"] == chelsea.name
    assert response.data[2]["team_name"] == liverpool.name
    assert response.data[1]["team_name"] == arsenal.name
