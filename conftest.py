import pytest
from rest_framework.test import APIClient
from leagues.models import League, Team

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_league(db):
    def _create_league(name, max_teams, **kwargs):
        return League.objects.create(name=name, max_teams=max_teams, **kwargs)
    return _create_league

@pytest.fixture
def sample_team(db):
    def _create_team(name, league, city, **kwargs):
        league = league or sample_league()
        return Team.objects.create(name=name, league=league, city=city, **kwargs)
    return _create_team

