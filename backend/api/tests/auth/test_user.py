import pytest
from django.contrib.auth.models import User
from django.core import mail
from rest_framework import status
from rest_framework.test import APIClient

from ...services.url import generate_reset_url


@pytest.mark.django_db
def test_user_get(user_valid: User, api_client: APIClient) -> None:
    response = api_client.get(f"/api/user/{user_valid.pk}/")
    assert response.status_code == status.HTTP_200_OK

    user = response.json()
    assert "id" in user
    assert "username" in user
    assert "email" in user
    assert "is_staff" in user
    assert "password" not in user


@pytest.mark.django_db
def test_user_get_not_found(api_client: APIClient) -> None:
    last_user = User.objects.last()
    unlikely_user_id = last_user.pk + 1 if last_user is not None else 1

    response = api_client.get(f"/api/user/{unlikely_user_id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_post(
    user_data_valid: dict[str, str], api_client: APIClient
) -> None:
    response = api_client.post("/api/user/", user_data_valid)
    assert response.status_code == status.HTTP_201_CREATED

    created_user = User.objects.get(username=user_data_valid["username"])

    assert created_user.email == user_data_valid["email"]
    assert not created_user.is_staff
    assert created_user.check_password(user_data_valid["password"])
    assert "password" not in response.data


@pytest.mark.django_db
def test_user_post_invalid_data(
    users_data_invalid: list, api_client: APIClient
):
    for user_data in users_data_invalid:
        response = api_client.post("/api/user/", user_data["data"])
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        if "error_message" in user_data:
            error_messages = list(response.data["password"])
            assert user_data["error_message"] in error_messages


@pytest.mark.django_db
def test_user_delete(user_valid: User, api_client: APIClient) -> None:
    api_client.force_authenticate(user=user_valid)
    response = api_client.delete(f"/api/user/{user_valid.pk}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_delete_not_found(api_client: APIClient) -> None:
    last_user = User.objects.last()
    unlikely_user_id = last_user.pk + 1 if last_user is not None else 1

    response = api_client.delete(f"/api/user/{unlikely_user_id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_delete_admin(
    user_admin: User, user_valid: User, api_client: APIClient
) -> None:
    api_client.force_authenticate(user=user_admin)

    response = api_client.delete(f"/api/user/{user_valid.pk}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_delete_other_user(
    users_valid: tuple[User, User], api_client: APIClient
) -> None:
    user1, user2 = users_valid
    api_client.force_authenticate(user=user1)

    response = api_client.delete(f"/api/user/{user2.pk}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_delete_own_account(
    user_valid: User, api_client: APIClient
) -> None:
    api_client.force_authenticate(user=user_valid)

    response = api_client.delete(f"/api/user/{user_valid.pk}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_delete_unauthenticated(
    user_valid: User, api_client: APIClient
) -> None:
    response = api_client.delete(f"/api/user/{user_valid.pk}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_update(
    user_valid: User,
    user_data_updated: dict[str, str],
    api_client: APIClient,
) -> None:
    api_client.force_authenticate(user=user_valid)

    response = api_client.patch(
        f"/api/user/{user_valid.pk}/", user_data_updated
    )
    assert response.status_code == status.HTTP_200_OK

    user_valid.refresh_from_db()

    for key in user_data_updated:
        if key != "password":
            assert getattr(user_valid, key) == user_data_updated[key]


@pytest.mark.django_db
def test_user_update_not_found(
    user_valid: User,
    user_data_updated: dict[str, str],
    api_client: APIClient,
) -> None:
    api_client.force_authenticate(user=user_valid)
    last_user = User.objects.last()
    unlikely_user_id = last_user.pk + 1 if last_user is not None else 1

    response = api_client.patch(
        f"/api/user/{unlikely_user_id}/", user_data_updated
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_update_invalid_data(
    user_admin: User, users_data_invalid: list, api_client: APIClient
):
    api_client.force_authenticate(user=user_admin)
    user_id = user_admin.pk

    for user_data in users_data_invalid:
        response = api_client.patch(f"/api/user/{user_id}/", user_data["data"])
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_update_admin(
    user_admin: User,
    user_valid: User,
    user_data_updated: dict[str, str],
    api_client: APIClient,
) -> None:
    api_client.force_authenticate(user=user_admin)
    response = api_client.patch(
        f"/api/user/{user_valid.pk}/", user_data_updated
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_update_other_user(
    users_valid: tuple[User, User],
    user_data_updated: dict[str, str],
    api_client: APIClient,
) -> None:
    user1, user2 = users_valid
    api_client.force_authenticate(user=user1)
    response = api_client.patch(f"/api/user/{user2.pk}/", user_data_updated)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_update_own_account(
    user_valid: User, user_data_updated: dict[str, str], api_client: APIClient
) -> None:
    api_client.force_authenticate(user=user_valid)
    response = api_client.patch(
        f"/api/user/{user_valid.pk}/", user_data_updated
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_update_unauthenticated(
    user_valid: User, user_data_updated: dict[str, str], api_client: APIClient
) -> None:
    response = api_client.patch(
        f"/api/user/{user_valid.pk}/", user_data_updated
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_users_get(
    users_valid: tuple[User, User], api_client: APIClient
) -> None:
    _, _ = users_valid
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
def test_reset_password_mail(user_valid: User, api_client: APIClient) -> None:
    response = api_client.post(
        "/api/user/reset-password/", {"email": user_valid.email}
    )
    assert response.status_code == status.HTTP_200_OK

    assert len(mail.outbox) == 1
    sent_mail = mail.outbox[0]
    assert "Сброс пароля" in sent_mail.subject
    assert (
        "Для сброса пароля перейдите по ссылке: "
        f"{generate_reset_url(user_valid)}" in sent_mail.body
    )
