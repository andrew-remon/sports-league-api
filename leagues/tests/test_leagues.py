# third-party
from django.urls import reverse
from rest_framework import status
import pytest

# local
from leagues.models import League


@pytest.mark.django_db
def test_list_league(api_client, sample_league):
    sample_league(name="Premier League", max_teams=20)
    sample_league(name="La Liga", max_teams=20)
    sample_league(name="Bundesliga", max_teams=18)
    url = reverse("league-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 3
    assert isinstance(response.data["results"], list)


@pytest.mark.django_db
def test_create_league(api_client):
    data = {"name": "Premier League", "max_teams": 20}
    url = reverse("league-list")
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data["name"]
    assert response.data["max_teams"] == data["max_teams"]
    assert League.objects.count() == 1
    league_id = response.data["id"]
    assert league_id is not None
    assert isinstance(league_id, int)
    created_league = League.objects.get(pk=league_id)
    assert created_league.name == data["name"]
    assert created_league.max_teams == data["max_teams"]


@pytest.mark.django_db
def test_create_league_invalid(api_client):
    data = {"name": "", "max_teams": 18}
    url = reverse("league-list")
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert League.objects.count() == 0


@pytest.mark.django_db
def test_create_league_duplicate_name(api_client, sample_league):
    sample_league(name="Premier League", max_teams=20)

    data = {"name": "Premier League", "max_teams": 20}
    url = reverse("league-list")
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert League.objects.count() == 1  # same as before, No insertions happened


@pytest.mark.django_db
def test_retrieve_league(api_client, sample_league):
    created_league = sample_league(name="Bundesliga", max_teams=18)

    url = reverse("league-detail", kwargs={"pk": created_league.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == created_league.name
    assert response.data["max_teams"] == created_league.max_teams


@pytest.mark.django_db
def test_retrieve_specific_league(api_client, sample_league):
    created_league = sample_league(name="Bundesliga", max_teams=18)

    response = api_client.get(f"/api/v1/leagues/{created_league.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == created_league.name
    assert response.data["max_teams"] == created_league.max_teams


@pytest.mark.django_db
def test_retrieve_nonexistent_league(api_client):
    response = api_client.get("/api/v1/leagues/999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_league(api_client, sample_league):
    created_league = sample_league(name="Premier League", max_teams=10)  # max_teams needs an update

    url = reverse("league-detail", kwargs={"pk": created_league.id})
    data = {"name": "Premier League", "max_teams": 20}
    response = api_client.put(url, data=data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert League.objects.count() == 1
    assert isinstance(response.data["id"], int)
    assert response.data["id"] == created_league.id
    assert response.data["name"] == data["name"]
    assert response.data["max_teams"] == data["max_teams"]

    created_league.refresh_from_db()
    assert created_league.max_teams == data["max_teams"]


@pytest.mark.django_db
def test_delete_league(api_client, sample_league):
    created_league = sample_league(name="Premier League", max_teams=18)

    url = reverse("league-detail", kwargs={"pk": created_league.id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not League.objects.filter(id=created_league.id).exists()
