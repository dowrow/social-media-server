from api.models import Publication
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, PublicationSerializer


class SelfDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response(UserSerializer(request.user).data)

    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SelfPublicationList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PublicationSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def get_queryset(self):
        return Publication.objects.filter(author=self.request.user)


class UserPublicationList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PublicationSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        return Publication.objects.filter(author=user)


class PublicationList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PublicationDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
