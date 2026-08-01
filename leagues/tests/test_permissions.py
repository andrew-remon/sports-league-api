# third-party
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
import pytest

# local
from leagues.models import League, Team, Match

def test_unauthenticated_can_read_leagues(unauthenticated_client, sample_league):
    sample_league(name="Premier League", max_teams=20)
    sample_league(name="La Liga", max_teams=20)
    url = reverse("league-list")

    response = unauthenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_unauthenticated_cannot_create_league(unauthenticated_client):
    data = {"name": "Premier League", "max_teams": 20}
    url = reverse("league-list")

    response = unauthenticated_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_authenticated_can_create_league(user_a_client, user_a):
    data = {"name": "Premier League", "max_teams": 20}
    url = reverse("league-list")

    response = user_a_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data

    league = League.objects.get(id=response.data["id"])
    assert league.name == data["name"]

@pytest.mark.django_db
def test_owner_can_update_league(user_a_client, user_a):
    created_league = League.objects.create(
        name="Original League Name",
        max_teams = 20,
        owner = user_a
    )

    url = reverse("league-detail", kwargs={"pk":created_league.id})

    updated_data = {
        "name":"Updated League Name",
    }

    response = user_a_client.patch(url, updated_data, format="json")

    assert response.status_code == status.HTTP_200_OK

    created_league.refresh_from_db()
    assert response.data["name"] == updated_data["name"]

@pytest.mark.django_db
def test_non_owner_cannot_update_league(user_b_client, user_a):
    created_league = League.objects.create(
        name="Original League Name",
        max_teams = 20,
        owner = user_a
    )

    url = reverse("league-detail", kwargs={"pk":created_league.id})

    updated_data = {
        "name":"Updated League Name",
    }

    response = user_b_client.patch(url, updated_data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_owner_can_delete_league(user_a_client, user_a):
    created_league = League.objects.create(
        name="Original League Name",
        max_teams = 20,
        owner = user_a
    )

    url = reverse("league-detail", kwargs={"pk":created_league.id})

    response = user_a_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_non_owner_cannot_delete_league(user_b_client, user_a):
    created_league = League.objects.create(
        name="Original League Name",
        max_teams = 20,
        owner = user_a
    )

    url = reverse("league-detail", kwargs={"pk":created_league.id})

    response = user_b_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_admin_can_update_any_league(admin_client, user_a):
    created_league = League.objects.create(
        name="Original League Name",
        max_teams = 20,
        owner = user_a
    )

    url = reverse("league-detail", kwargs={"pk":created_league.id})

    updated_data = {
        "name":"Updated League Name",
    }

    response = admin_client.patch(url, updated_data, format="json")

    assert response.status_code == status.HTTP_200_OK

    created_league.refresh_from_db()
    assert response.data["name"] == updated_data["name"]

@pytest.mark.django_db
def test_owner_can_add_team_to_league(user_a_client, user_a):
    created_league = League.objects.create(
        name = "Premier League",
        max_teams = 20,
        owner= user_a
    )

    data = {
        "name":"Man City",
        "city":"Manchester",
        "league":created_league.id
    }

    url = reverse("team-list")

    response = user_a_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_non_owner_cannot_add_team_to_league(user_b_client, user_a):
    created_league = League.objects.create(
        name = "Premier League",
        max_teams = 20,
        owner= user_a
    )

    data = {
        "name":"Man City",
        "city":"Manchester",
        "league":created_league.id
    }

    url = reverse("team-list")

    response = user_b_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_owner_can_schedule_match(user_a, user_a_client):
    league = League.objects.create(
        name="Premier League",
        max_teams = 20,
        owner = user_a
    )

    team_a = Team.objects.create(
        name="Man City",
        city="Manchester",
        league=league
    )

    team_b = Team.objects.create(
        name="Liverpool",
        city="Liverpool",
        league=league
    )

    data = {
        "league":league.id,
        "home_team":team_a.id,
        "away_team":team_b.id,
        "status":"scheduled",
        "match_day":4
    }

    url = reverse("match-list")

    response = user_a_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    # print("\nVALIDATION ERRORS:", response.data)

@pytest.mark.django_db
def test_owner_can_record_result(user_a, user_a_client):
    league = League.objects.create(
        name="Premier League",
        max_teams = 20,
        owner = user_a
    )

    team_a = Team.objects.create(
        name="Man City",
        city="Manchester",
        league=league
    )

    team_b = Team.objects.create(
        name="Liverpool",
        city="Liverpool",
        league=league
    )

    match = Match.objects.create(
        league=league,
        home_team=team_a,
        away_team=team_b,
        status=Match.MatchStatus.SCHEDULED,
        match_day=4
    )

    data = {
        "home_score":4,
        "away_score":2,
    }

    url = reverse("match-record-result", kwargs={"pk":match.id})

    response = user_a_client.post(url, data, format="json")

    assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]

@pytest.mark.django_db
def test_non_owner_cannot_record_result(user_a, user_b_client):
    league = League.objects.create(
        name="Premier League",
        max_teams = 20,
        owner = user_a
    )

    team_a = Team.objects.create(
        name="Man City",
        city="Manchester",
        league=league
    )

    team_b = Team.objects.create(
        name="Liverpool",
        city="Liverpool",
        league=league
    )

    match = Match.objects.create(
        league=league,
        home_team=team_a,
        away_team=team_b,
        status=Match.MatchStatus.SCHEDULED,
        match_day=4
    )

    data = {
        "home_score":4,
        "away_score":2,
    }

    url = reverse("match-record-result", kwargs={"pk":match.id})

    response = user_b_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
