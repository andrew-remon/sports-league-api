# stdlib
from datetime import timedelta

# third-party
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
import pytest

# local
from leagues.models import Match


@pytest.mark.django_db
def test_filter_teams_by_league(api_client, sample_league, sample_team):
    league_a = sample_league(name="Premier League", max_teams=20)
    league_b = sample_league(name="La Liga", max_teams=20)
    team_a = sample_team(name="Man City", league=league_a, city="Manchester")
    sample_team(name="Real Madrid", league=league_b, city="Madrid")
    url = reverse("team-list")
    response = api_client.get(url, data={"league": league_a.id})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["name"] == team_a.name


@pytest.mark.django_db
def test_search_players_by_name(api_client, sample_player, sample_team, sample_league):
    league_b = sample_league(name="La Liga", max_teams=20)
    team_a = sample_team(name="Real Madrid", league=league_b, city="Madrid")
    team_b = sample_team(name="Barcelona", league=league_b, city="Barcelona")
    p1 = sample_player(
        first_name="Kilian",
        last_name="Mbappe",
        team=team_a,
        jersey_number=9,
        position="FWD",
    )
    sample_player(
        first_name="Jude",
        last_name="Bellingham",
        team=team_a,
        jersey_number=5,
        position="MID",
    )
    sample_player(
        first_name="Lamine",
        last_name="Yamal",
        team=team_b,
        jersey_number=19,
        position="FWD",
    )
    url = reverse("player-list")
    response = api_client.get(url, data={"search": "kili"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["first_name"] == p1.first_name


@pytest.mark.django_db
def test_ordering_matches_by_date(api_client, sample_league, sample_team, sample_match):
    league = sample_league(name="Premier League", max_teams=20)
    team_a = sample_team(name="Man City", league=league, city="Manchester")
    team_b = sample_team(name="Liverpool", league=league, city="Liverpool")
    team_c = sample_team(name="Arsenal", league=league, city="London")

    now = timezone.now()
    date_today = now
    date_tomorrow = now + timedelta(days=1)
    date_yesterday = now - timedelta(days=1)

    m1 = sample_match(
        league=league,
        home_team=team_a,
        away_team=team_b,
        match_day=1,
        status=Match.MatchStatus.SCHEDULED,
        scheduled_date=date_today,
    )
    m2 = sample_match(
        league=league,
        home_team=team_b,
        away_team=team_c,
        match_day=2,
        status=Match.MatchStatus.SCHEDULED,
        scheduled_date=date_tomorrow,
    )
    m3 = sample_match(
        league=league,
        home_team=team_c,
        away_team=team_a,
        match_day=3,
        status=Match.MatchStatus.SCHEDULED,
        scheduled_date=date_yesterday,
    )

    url = reverse("match-list")

    # 4. Test Ascending Order (ordering=scheduled_date)
    response = api_client.get(url, data={"ordering": "scheduled_date"})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == 3
    assert results[0]["id"] == m3.id
    assert results[1]["id"] == m1.id
    assert results[2]["id"] == m2.id

    # 5. Test Descending Order (ordering=-scheduled_date)
    response = api_client.get(url, data={"ordering": "-scheduled_date"})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == 3
    assert results[0]["id"] == m2.id
    assert results[1]["id"] == m1.id
    assert results[2]["id"] == m3.id
