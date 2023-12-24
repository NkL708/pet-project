from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user import UserSerializer


class UserListView(APIView):
    def get(self, _) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
