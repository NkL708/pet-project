from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HelloWorldSerializer

class HelloWorldView(APIView):
    def get(self, request, format=None):
        serializer = HelloWorldSerializer()
        return Response(serializer.data, status=status.HTTP_200_OK)