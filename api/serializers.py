from django.contrib.auth.models import User
from rest_framework import serializers
from social.apps.django_app.default.models import UserSocialAuth
from .models import Publication, Follow


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    publications_count = serializers.SerializerMethodField()
    followed = serializers.SerializerMethodField()

    def get_followed(self, user):
        current_user = self.context['request'].user
        return Follow.objects.filter(follower=current_user, followed=user).exists()

    def get_publications_count(self, user):
        return Publication.objects.filter(author=user).count()

    def get_profile_picture(self, user):
        try:
            user_social_auth = UserSocialAuth.objects.get(user=user)

            if user_social_auth.provider == 'facebook':
                return 'https://graph.facebook.com/' + user_social_auth.uid + '/picture?type=normal'
            elif user_social_auth.provider == 'twitter':
                return 'https://twitter.com/' + user.username + '/profile_image?size=bigger'
        except:
            return ''

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'profile_picture', 'publications_count', 'followed')


class PublicationSerializer(serializers.ModelSerializer):
    author_details = serializers.SerializerMethodField()

    def get_author_details(self, publication):
        return UserSerializer(publication.author, context=self.context).data

    class Meta:
        model = Publication
        fields = ('id', 'author_details', 'timestamp', 'image', 'text', )
        read_only_fields = ('author',)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ('follower',)