import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username='testuser', password='testpass')
    assert user.username == 'testuser'
    assert user.check_password('testpass')
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_token_obtain_pair():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    response = client.post('/api/token/', {'username': user.username,
                                           'password': 'testpass'})
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_refresh_token():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    response = client.post('/api/token/', {'username': user.username,
                                           'password': 'testpass'})
    assert response.status_code == 200

    access_token = response.data['access']
    refresh_token = response.data['refresh']
    response = client.post('/api/token/refresh/', {'refresh': refresh_token})
    assert response.status_code == 200
    new_access_token = response.data['access']
    assert new_access_token != access_token


@pytest.mark.django_db
def test_verify_token():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    response = client.post('/api/token/', {'username': user.username,
                                           'password': 'testpass'})
    assert response.status_code == 200
    access_token = response.data['access']

    response = client.post('/api/token/verify/', {'token': access_token})
    assert response.status_code == 200
