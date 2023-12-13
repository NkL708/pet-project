from django.core.mail import send_mail
from django.conf import settings


def send_reset_password_email(email: str, url: str) -> None:
    subject = "Сброс пароля"
    message = f"Для сброса пароля перейдите по ссылке: {url}"
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email], False)
