import pytest
from rest_framework.test import APIClient
from leagues.models import League, Team, Player, Match

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_league(db):
    def _create_league(name, max_teams, **kwargs):
        return League.objects.create(
            name=name,
            max_teams=max_teams,
            **kwargs)
    return _create_league

@pytest.fixture
def sample_team(db):
    def _create_team(name, league, city, **kwargs):
        league = league or sample_league()
        return Team.objects.create(
            name=name,
            league=league,
            city=city,
            **kwargs)
    return _create_team

@pytest.fixture
def sample_player(db):
    def _create_player(first_name, last_name, team, jersey_number, position, **kwargs):
        return Player.objects.create(
            first_name=first_name,
            last_name=last_name,
            team=team,
            jersey_number=jersey_number,
            position=position,
            **kwargs)
    return _create_player

@pytest.fixture
def sample_match(db):
    def _create_match(league, home_team, away_team, match_day, status, scheduled_date=None, **kwargs):
        return Match.objects.create(
            league=league,
            home_team=home_team,
            away_team=away_team,
            match_day=match_day,
            status=status,
            scheduled_date=scheduled_date,
            **kwargs
        )
    return _create_match
