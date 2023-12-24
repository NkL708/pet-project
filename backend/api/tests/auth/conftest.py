# pylint: disable=redefined-outer-name
# pylint: disable=too-few-public-methods
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .factory import UserDictFactory, UserFactory


@pytest.fixture
def api_client() -> APIClient:
    api_client = APIClient()
    api_client.default_format = "json"
    return api_client


@pytest.fixture
def user_valid() -> User:
    return UserFactory()


@pytest.fixture
def user_admin() -> User:
    return UserFactory(username="admin", is_staff=True)


@pytest.fixture
def users_valid() -> tuple[User, User]:
    return UserFactory(), UserFactory()


@pytest.fixture
def user_data_valid() -> dict[str, str]:
    return UserDictFactory()


@pytest.fixture
def users_data_invalid_password() -> list:
    invalid_password_data = [
        (
            "",
            "The password is too similar to the username.",
            "UserAttributeSimilarityValidator",
        ),
        (
            "short",
            (
                "This password is too short. It must contain at least "
                "8 characters."
            ),
            "MinimumLengthValidator",
        ),
        (
            "password",
            "This password is too common.",
            "CommonPasswordValidator",
        ),
        (
            "12345678",
            "This password is entirely numeric.",
            "NumericPasswordValidator",
        ),
    ]

    users_data = []
    for password, error_message, validator in invalid_password_data:
        user_data = UserDictFactory.build()
        user_data["password"] = password
        if validator == "UserAttributeSimilarityValidator":
            user_data["password"] = user_data["username"]
        users_data.append({"data": user_data, "error_message": error_message})

    return users_data


@pytest.fixture
def users_data_invalid_email() -> list:
    invalid_email_data = [
        (""),
        ("user@examplecom"),
        ("user@exa mple.com"),
        (".user@example.com"),
    ]

    users_data = []
    for email in invalid_email_data:
        user_data = UserDictFactory.build()
        user_data["email"] = email
        users_data.append({"data": user_data})

    return users_data


@pytest.fixture
def users_data_invalid_username() -> list:
    invalid_username_data = [
        (""),
        ("user_name!"),
        ("user name"),
    ]

    users_data = []
    for username in invalid_username_data:
        user_data = UserDictFactory.build()
        user_data["username"] = username
        users_data.append({"data": user_data})

    return users_data


@pytest.fixture
def users_data_invalid(
    users_data_invalid_username: list,
    users_data_invalid_password: list,
    users_data_invalid_email: list,
) -> list:
    return (
        users_data_invalid_username
        + users_data_invalid_password
        + users_data_invalid_email
    )


@pytest.fixture
def user_data_updated(user_data_valid: dict[str, str]) -> dict[str, str]:
    return {
        key: f"new-{value}"
        for key, value in user_data_valid.items()
        if key != "is_staff"
    }
