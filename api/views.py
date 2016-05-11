from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_social_oauth2 import authentication

from .serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class Login(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        return Response(UserSerializer(request.user).data)