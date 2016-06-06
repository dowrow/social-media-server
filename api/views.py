from api.models import Publication, Follow
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, PublicationSerializer, FollowSerializer


class SelfDetail(APIView):
    def get(self, request, format=None):
        return Response(UserSerializer(request.user).data)

    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
    def get(self, request, pk, format=None):
        return Response(UserSerializer(User.objects.get(pk=pk)).data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username',)
    ordering = '-username'


class SelfPublicationList(generics.ListAPIView):
    serializer_class = PublicationSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def get_queryset(self):
        return Publication.objects.filter(author=self.request.user)


class UserPublicationList(generics.ListAPIView):
    serializer_class = PublicationSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        return Publication.objects.filter(author=user)


class PublicationList(generics.ListCreateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PublicationDetail(generics.RetrieveDestroyAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class FollowList(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def perform_create(self, serializer):
        current_user = self.request.user
        queryset = Follow.objects.filter(follower=current_user, followed=self.request.POST['followed'])
        if queryset.exists():
            raise APIException('Follow relationship already exists')
        else:
            serializer.save(follower=self.request.user)


class FollowDetail(generics.RetrieveDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

