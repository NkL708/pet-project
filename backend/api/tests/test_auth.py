from django.contrib.auth.models import User
from django.core import mail
from rest_framework.test import APIClient
from rest_framework import status
import pytest

from ..services.url import generate_reset_url


@pytest.mark.django_db
def test_user_get(test_user: User, api_client: APIClient) -> None:
    response = api_client.get(f"/api/user/{test_user.id}/")
    assert response.status_code == status.HTTP_200_OK

    user = response.json()
    assert "id" in user
    assert "username" in user
    assert "email" in user
    assert "is_staff" in user
    assert "password" not in user


@pytest.mark.django_db
def test_user_get_not_found(api_client: APIClient) -> None:
    unlikely_user_id = 999999
    response = api_client.get(f"/api/user/{unlikely_user_id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_post(user_data: dict[str, str], api_client: APIClient) -> None:
    response = api_client.post("/api/user/", user_data)
    assert response.status_code == status.HTTP_201_CREATED

    created_user = User.objects.get(username=user_data["username"])
    assert created_user.email == user_data["email"]

    assert not created_user.is_staff
    assert created_user.check_password(user_data["password"])


@pytest.mark.django_db
def test_user_post_invalid_data(
    invalid_user_data: list[dict[str, any]], api_client: APIClient
) -> None:
    for user_data in invalid_user_data:
        response = api_client.post("/api/user/", user_data["data"])
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        error_messages = list(response.data["password"])
        assert user_data["error_message"] in error_messages


@pytest.mark.django_db
def test_user_delete(test_user: User, api_client: APIClient) -> None:
    api_client.force_authenticate(user=test_user)
    response = api_client.delete(f"/api/user/{test_user.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_delete_not_found(api_client: APIClient) -> None:
    unlikely_user_id = 9999999
    response = api_client.delete(f"/api/user/{unlikely_user_id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_delete_admin(
    admin_user: User, test_user: User, api_client: APIClient
) -> None:
    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(f"/api/user/{test_user.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_delete_other_user(
    test_users: tuple[User, User], api_client: APIClient
) -> None:
    user1, user2 = test_users
    api_client.force_authenticate(user=user1)

    response = api_client.delete(f"/api/user/{user2.id}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_delete_own_account(
    test_user: User, api_client: APIClient
) -> None:
    api_client.force_authenticate(user=test_user)

    response = api_client.delete(f"/api/user/{test_user.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_delete_unauthenticated(
    test_user: User, api_client: APIClient
) -> None:
    response = api_client.delete(f"/api/user/{test_user.id}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_update(
    test_user: User,
    updated_user_data: dict[str, str],
    api_client: APIClient,
) -> None:
    api_client.force_authenticate(user=test_user)

    response = api_client.patch(
        f"/api/user/{test_user.id}/", updated_user_data
    )
    assert response.status_code == status.HTTP_200_OK

    test_user.refresh_from_db()

    for key in updated_user_data:
        if key != "password":
            assert getattr(test_user, key) == updated_user_data[key]


@pytest.mark.django_db
def test_user_update_not_found(
    test_user: User,
    updated_user_data: dict[str, str],
    api_client: APIClient,
) -> None:
    api_client.force_authenticate(user=test_user)
    unlikely_user_id = 999999

    response = api_client.patch(
        f"/api/user/{unlikely_user_id}/", updated_user_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_update_invalid_data(
    admin_user: User,
    api_client: APIClient,
    invalid_user_data: list[dict[str, any]],
    user_data: dict[str, str],
) -> None:
    api_client.force_authenticate(user=admin_user)
    for index, obj in enumerate(invalid_user_data):
        unique_user_data = user_data.copy()
        unique_user_data["username"] = f"{user_data['username']}{index}"
        user = User.objects.create_user(**unique_user_data)

        response = api_client.patch(f"/api/user/{user.id}/", obj["data"])
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert obj["error_message"] in response.data["password"]


@pytest.mark.django_db
def test_user_update_admin(
    admin_user: User,
    test_user: User,
    updated_user_data: dict[str, str],
    api_client: APIClient,
) -> None:
    api_client.force_authenticate(user=admin_user)
    response = api_client.patch(
        f"/api/user/{test_user.id}/", updated_user_data
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_update_other_user(
    test_users: tuple[User, User],
    updated_user_data: dict[str, str],
    api_client: APIClient,
) -> None:
    user1, user2 = test_users
    api_client.force_authenticate(user=user1)
    response = api_client.patch(f"/api/user/{user2.id}/", updated_user_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_update_own_account(
    test_user: User, updated_user_data: dict[str, str], api_client: APIClient
) -> None:
    api_client.force_authenticate(user=test_user)
    response = api_client.patch(
        f"/api/user/{test_user.id}/", updated_user_data
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_update_unauthenticated(
    test_user: User, updated_user_data: dict[str, str], api_client: APIClient
) -> None:
    response = api_client.patch(
        f"/api/user/{test_user.id}/", updated_user_data
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_users_get(
    test_users: tuple[User, User], api_client: APIClient
) -> None:
    _, _ = test_users
    response = api_client.get("/api/users/")
    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 2

    for user in response.json():
        assert "id" in user
        assert "username" in user
        assert "email" in user
        assert "is_staff" in user
        assert "password" not in user


@pytest.mark.django_db
def test_reset_password_mail(test_user: User, api_client: APIClient) -> None:
    response = api_client.post(
        "/api/user/reset-password/", {"email": test_user.email}
    )
    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    sent_mail = mail.outbox[0]
    assert "Сброс пароля" in sent_mail.subject
    assert (
        "Для сброса пароля перейдите по ссылке: "
        f"{generate_reset_url(test_user)}" in sent_mail.body
    )


@pytest.mark.django_db
def test_reset_password_wrong_password(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/user/reset-password/", {"email": "wrongemail@example.com"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
