from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse


def generate_reset_url(user: User) -> str:
    uid = user.pk
    token = default_token_generator.make_token(user)
    url = reverse("reset-password")
    reset_password_url = f"{url}{uid}/{token}"
    return reset_password_url
