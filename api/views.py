from api.models import Publication, Follow
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, PublicationSerializer, FollowSerializer


class SelfDetail(APIView):
    def get(self, request, format=None):
        return Response(UserSerializer(request.user, context={'request': request}).data)

    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
    def get(self, request, pk, format=None):
        return Response(UserSerializer(User.objects.get(pk=pk), context={'request': request}).data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username',)
    ordering = '-username'

    def get_serializer_context(self):
        return {'request': self.request}


class SelfPublicationList(generics.ListAPIView):
    serializer_class = PublicationSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def get_queryset(self):
        return Publication.objects.filter(author=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}


class UserPublicationList(generics.ListAPIView):
    serializer_class = PublicationSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs.get('pk'))
        return Publication.objects.filter(author=user)

    def get_serializer_context(self):
        return {'request': self.request}


class PublicationList(generics.ListCreateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}


class HomePublicationList(generics.ListAPIView):
    serializer_class = PublicationSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = '-timestamp'

    def get_queryset(self):
        followed_users = Follow.objects.filter(follower=self.request.user).values('followed')
        return Publication.objects.filter(author__in=followed_users)

    def get_serializer_context(self):
        return {'request': self.request}


class PublicationDetail(generics.RetrieveDestroyAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class FollowUser(APIView):
    def post(self, request, pk, format=None):
        follower = request.user
        followed = User.objects.get(pk=pk)
        queryset = Follow.objects.filter(follower=follower, followed=followed)
        if queryset.exists():
            raise APIException('Follow relationship already exists')
        else:
            follow = Follow.objects.create(follower=follower, followed=followed)
            follow.save()
            return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)


class UnfollowUser(APIView):
    def delete(self, request, follower_pk, followed_pk, format=None):
        follower = User.objects.get(pk=follower_pk)
        followed = User.objects.get(pk=followed_pk)
        if follower.id != request.user.id:
            raise APIException('Access denied')
        follow = Follow.objects.get(follower=follower, followed=followed)
        if follow is not None:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise APIException('Follow does not exists')


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
