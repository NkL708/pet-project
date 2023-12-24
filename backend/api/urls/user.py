from django.urls import path

from ..views.user import UserView, reset_password

urlpatterns = [
    path("<int:user_id>/", UserView.as_view()),
    path("", UserView.as_view()),
    path("reset-password/", reset_password, name="reset-password"),
]
