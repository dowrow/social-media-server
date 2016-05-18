from api.models import Publication
from django.contrib.auth.models import User
from rest_framework import serializers
from social.apps.django_app.default.models import UserSocialAuth
from .models import Publication


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, user):
        user_social_auth = UserSocialAuth.objects.get(user=user)
        if user_social_auth.provider == 'facebook':
            return 'https://graph.facebook.com/' + user_social_auth.uid + '/picture?type=normal'
        elif user_social_auth.provider == 'twitter':
            return 'https://twitter.com/' + user.username + '/profile_image?size=bigger'

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'profile_picture')


class PublicationSerializer(serializers.ModelSerializer):
    author_details = serializers.SerializerMethodField()

    def get_author_details(self, publication):
        return UserSerializer(publication.author).data

    class Meta:
        model = Publication
        fields = ('id', 'author_details', 'timestamp', 'image', 'text', )
        read_only_fields = ('author',)

