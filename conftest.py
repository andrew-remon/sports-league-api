# third-party
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

# local
from leagues.models import League, Team, Player, Match


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


@pytest.fixture
def sample_player(db):
    def _create_player(first_name, last_name, team, jersey_number, position, **kwargs):
        return Player.objects.create(
            first_name=first_name,
            last_name=last_name,
            team=team,
            jersey_number=jersey_number,
            position=position,
            **kwargs,
        )

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
            **kwargs,
        )

    return _create_match

@pytest.fixture
def user_factory(db, django_user_model):
    def _create_user(email="test@example.com", password="Password123!", is_staff=False):
        return django_user_model.objects.create(
            email=email,
            password=password,
            is_staff=is_staff
        )
    return _create_user

@pytest.fixture
def user_a(user_factory):
    return user_factory(email="user_a@example.com")

@pytest.fixture
def user_b(user_factory): # defines DB model instance User
    return user_factory(email="user_b@example.com")

@pytest.fixture
def user_a_client(api_client, user_a): # defines the HTTP api client
    client = api_client
    token = RefreshToken.for_user(user_a).access_token
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client

@pytest.fixture
def user_b_client(api_client, user_b): # defines the HTTP api client
    client = api_client
    token = RefreshToken.for_user(user_b).access_token
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client

@pytest.fixture
def admin_user(user_factory):
    return user_factory(email="admin@example.com", is_staff=True)

@pytest.fixture
def admin_client(api_client, admin_user):
    client = api_client
    token = RefreshToken.for_user(admin_user).access_token
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client

@pytest.fixture
def unauthenticated_client():
    return APIClient()
