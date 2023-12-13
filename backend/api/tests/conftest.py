# pylint: disable=redefined-outer-name
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def test_user() -> User:
    return User.objects.create_user(
        username="testuser",
        password="StrongP@ssw0rd123",
        email="test@example.com",
    )


@pytest.fixture
def admin_user() -> User:
    return User.objects.create_user(
        username="admin",
        password="StrongP@ssw0rd",
        email="test@example.com",
        is_staff="True",
    )


@pytest.fixture
def test_users() -> tuple[User, User]:
    user1 = User.objects.create_user(
        username="testuser1",
        password="StrongP@ssw0rd123",
        email="test1@example.com",
    )
    user2 = User.objects.create_user(
        username="testuser2",
        password="StrongP@ssw0rd123",
        email="test2@example.com",
    )
    return user1, user2


@pytest.fixture
def api_client() -> APIClient:
    api_client = APIClient()
    api_client.default_format = "json"
    return api_client


@pytest.fixture
def user_data() -> dict[str, str]:
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongP@ssw0rd123",
    }


@pytest.fixture
def invalid_user_data() -> list[dict[str, any]]:
    return [
        {
            "data": {
                "username": "testuser",
                "email": "user@example.com",
                "password": "testuser",
            },
            "error_message": "The password is too similar to the username.",
        },
        {
            "data": {
                "username": "user123",
                "email": "user123@example.com",
                "password": "short",
            },
            "error_message": (
                "This password is too short. "
                "It must contain at least 8 characters."
            ),
        },
        {
            "data": {
                "username": "commonuser",
                "email": "commonuser@example.com",
                "password": "password",
            },
            "error_message": "This password is too common.",
        },
        {
            "data": {
                "username": "numericuser",
                "email": "numericuser@example.com",
                "password": "12345678",
            },
            "error_message": "This password is entirely numeric.",
        },
    ]


@pytest.fixture
def updated_user_data(user_data: dict[str, str]) -> dict[str, str]:
    return {key: f"new-{value}" for key, value in user_data.items()}
