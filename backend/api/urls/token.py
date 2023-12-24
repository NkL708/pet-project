from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path("", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("verify/", TokenVerifyView.as_view()),
]
