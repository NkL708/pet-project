from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user import ResetPasswordSerializer, UserSerializer
from ..services.mail import send_reset_password_email
from ..services.url import generate_reset_url


class UserView(APIView):
    @permission_classes([AllowAny])
    def get(self, _: Request, user_id: int) -> Response:
        user = get_object_or_404(User, pk=user_id)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    @permission_classes([AllowAny])
    def post(self, request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated])
    def delete(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, pk=user_id)

        if not (request.user == user or request.user.is_staff):  # type: ignore
            return Response(status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @permission_classes([IsAuthenticated])
    def put(self, request: Request, user_id: int) -> Response:
        return self._update_user(request, user_id, partial_update=False)

    @permission_classes([IsAuthenticated])
    def patch(self, request: Request, user_id: int) -> Response:
        return self._update_user(request, user_id, partial_update=True)

    def _update_user(
        self, request: Request, user_id: int, partial_update: bool
    ) -> Response:
        user = get_object_or_404(User, pk=user_id)
        if not (request.user == user or request.user.is_staff):  # type: ignore
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(
            user, data=request.data, partial=partial_update
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def reset_password(request: Request) -> Response:
    serializer = ResetPasswordSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        url = generate_reset_url(user)
        send_reset_password_email(email, url)
        return Response(status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
