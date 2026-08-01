# stdlib
from datetime import datetime, timedelta, timezone

# third-party
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
import pytest

User = get_user_model()

@pytest.mark.django_db
def test_register_success(unauthenticated_client):
    url = reverse("register")

    payload = {
        "email":"newuser@example.com",
        "password":"SecurePassword1234!",
        "first_name":"Test",
        "last_name":"User",
    }

    response = unauthenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["email"] == payload["email"]
    assert "password" not in response.data

    # assert payload saved in db correctly
    user = User.objects.get(email=payload["email"])
    assert user is not None
    assert user.check_password(payload["password"])

@pytest.mark.django_db
def test_register_duplicate_email(unauthenticated_client):
    url = reverse("register")

    duplicate_email = "newuser@example.com"

    User.objects.create_user(
        email=duplicate_email,
        password="OriginalPassword1234!",
        first_name = "Test",
        last_name = "DuplicateUser",
    )

    payload = {
        "email": duplicate_email,
        "password":"SecurePassword1234!",
        "first_name":"Test",
        "last_name":"User",
    }

    response = unauthenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_register_weak_password(unauthenticated_client):
    url = reverse("register")

    payload = {
        "email":"newuser@example.com",
        "password":"12345",
        "first_name":"Test",
        "last_name":"User",
    }

    response = unauthenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_login_success(unauthenticated_client):
    url = reverse("login")

    User.objects.create_user(
        email="newuser@example.com",
        password="OriginalPassword1234!",
        first_name = "Test",
        last_name = "DuplicateUser",
    )

    payload = {
        "email":"newuser@example.com",
        "password":"OriginalPassword1234!",
    }

    response = unauthenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data

    assert isinstance(response.data["access"], str) and len(response.data["access"]) > 0
    assert isinstance(response.data["refresh"], str) and len(response.data["refresh"]) > 0

@pytest.mark.django_db
def test_login_wrong_password(unauthenticated_client):
    url = reverse("login")

    User.objects.create_user(
        email="newuser@example.com",
        password="OriginalPassword1234!",
        first_name = "Test",
        last_name = "DuplicateUser",
    )

    payload = {
        "email":"newuser@example.com",
        "password":"OriginalPassword", # forget 1234! at the end
    }

    response = unauthenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_login_nonexistent_email(unauthenticated_client):
    url = reverse("login")

    User.objects.create_user(
        email="newuser@example.com",
        password="OriginalPassword1234!",
        first_name = "Test",
        last_name = "DuplicateUser",
    )

    payload = {
        "email": "nonexistentemail@example.com",
        "password":"OriginalPassword1234!",
    }

    response = unauthenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_refresh_token(unauthenticated_client):
    url = reverse("refresh")

    user = User.objects.create_user(
        email="newuser@example.com",
        password="OriginalPassword1234!",
        first_name = "Test",
        last_name = "User",
    )
    refresh_token = RefreshToken.for_user(user)

    payload = {
        "refresh" : str(refresh_token)
    }

    response = unauthenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert isinstance(response.data["access"], str) and len(response.data["access"]) > 0

@pytest.mark.django_db
def test_refresh_expired_token(unauthenticated_client):
    url = reverse("refresh")

    user = User.objects.create_user(
        email="newuser@example.com",
        password="OriginalPassword1234!",
        first_name = "Test",
        last_name = "User",
    )
    refresh_token = RefreshToken.for_user(user)

    past_time = datetime.now(timezone.utc) - timedelta(days=1)
    refresh_token["exp"] = int(past_time.timestamp())

    payload = {
        "refresh": str(refresh_token)
    }

    response = unauthenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_logout_blacklists_refresh(user_a_client, user_a):
    refresh_token = RefreshToken.for_user(user_a)

    logout_url = reverse("logout")
    refresh_url = reverse("refresh")

    payload = {
        "refresh": str(refresh_token)
    }

    logout_response = user_a_client.post(logout_url, payload, format="json")
    assert logout_response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT, status.HTTP_205_RESET_CONTENT]

    refresh_response = user_a_client.post(refresh_url, payload, format="json")
    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED

    assert BlacklistedToken.objects.filter(token__token=str(refresh_token)).exists()

def test_profile_authenticated(user_a_client):
    url = reverse("profile")

    response = user_a_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "email" in response.data
    assert "first_name" in response.data
    assert "password" not in response.data

def test_profile_unauthenticated(unauthenticated_client):
    url = reverse("profile")

    response = unauthenticated_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
