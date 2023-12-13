from django.urls import path
from ..views.user import reset_password, UserView


urlpatterns = [
    path("<int:user_id>/", UserView.as_view()),
    path("", UserView.as_view()),
    path("reset-password/", reset_password, name="reset-password"),
]
