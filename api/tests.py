import json

from api.models import Publication
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from social.apps.django_app.default.models import UserSocialAuth

ROOT_PATH = '/api/v0'
USERS_PATH = ROOT_PATH + '/users/'
SELF_PATH = USERS_PATH + 'self/'
PUBLICATIONS_PATH = ROOT_PATH + '/publications/'
SELF_PUBLICATIONS_PATH = SELF_PATH + 'publications/'

class SelfDetailTests(APITestCase):
    def setUp(self):
        test_user = User.objects.create(username='test', email='email@test.com')
        test_user.set_password('password')
        test_user.save()
        test_user_social_auth = UserSocialAuth.objects.create(user=test_user, provider='facebook', uid='10153580114080777')
        test_user_social_auth.save()

    @staticmethod
    def test_get_fail():
        client = APIClient()
        response = client.get(SELF_PATH)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        client.logout()

    @staticmethod
    def test_get_ok():
        client = APIClient()
        test_user = User.objects.get(username='test')
        client.force_authenticate(test_user)
        response = client.get(SELF_PATH)
        print response
        assert response.status_code == status.HTTP_200_OK

    @staticmethod
    def test_delete():
        client = APIClient()
        test_user = User.objects.get(username='test')
        client.force_authenticate(test_user)
        response = client.delete(SELF_PATH)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.filter(username='test').exists() == False


class PublicationListTests(APITestCase):
    IMAGE_PATH = 'test.jpg'
    TEST_IMAGE = SimpleUploadedFile(name='test.jpg', content=open(IMAGE_PATH, 'rb').read(), content_type='image/jpeg');

    def setUp(self):
        test_user = User.objects.create(username='test', email='email@test.com')
        test_user.set_password('password')
        test_user.save()
        test_user_social_auth = UserSocialAuth.objects.create(user=test_user, provider='facebook', uid='10153580114080777')
        test_user_social_auth.save()
        test_user2 = User.objects.create(username='test2', email='email2@test.com')
        test_user2.set_password('password2')
        test_user2.save()
        test_user_social_auth2 = UserSocialAuth.objects.create(user=test_user2, provider='twitter', uid='162377671')
        test_user_social_auth2.save()
        test_publication = Publication.objects.create(text="Test title 1", author=test_user, image=self.TEST_IMAGE)
        test_publication2 = Publication.objects.create(text="Test title 2", author=test_user2, image=self.TEST_IMAGE)
        test_publication.save()
        test_publication2.save()

    def test_get_ok(self):
        client = APIClient()
        test_user = User.objects.get(username='test')
        client.force_authenticate(test_user)
        response = client.get(PUBLICATIONS_PATH + '?cursor=')
        print response
        assert response.status_code == status.HTTP_200_OK

    def test_post_delete_ok(self):
        client = APIClient()
        test_user = User.objects.get(username='test')
        client.force_authenticate(test_user)
        response = client.post(PUBLICATIONS_PATH, {
            'text': 'Test title 3',
            'image': File(open(self.IMAGE_PATH))
        })
        assert response.status_code == status.HTTP_201_CREATED
        id = json.loads(response.content)['id']
        response = client.delete(PUBLICATIONS_PATH + str(id) + '/')
        print response
        assert response.status_code == status.HTTP_204_NO_CONTENT


class SelfPublicationList(APITestCase):
    IMAGE_PATH = 'test.jpg'
    TEST_IMAGE = SimpleUploadedFile(name='test.jpg', content=open(IMAGE_PATH, 'rb').read(), content_type='image/jpeg');

    def setUp(self):
        test_user = User.objects.create(username='test', email='email@test.com')
        test_user.set_password('password')
        test_user.save()
        test_user_social_auth = UserSocialAuth.objects.create(user=test_user, provider='facebook', uid='10153580114080777')
        test_user_social_auth.save()
        test_publication = Publication.objects.create(text="Test title 1", author=test_user, image=self.TEST_IMAGE)
        test_publication.save()

    def test_get_ok(self):
        client = APIClient()
        test_user = User.objects.get(username='test')
        client.force_authenticate(test_user)
        response = client.get(SELF_PUBLICATIONS_PATH + '?cursor=')
        print response
        assert response.status_code == status.HTTP_200_OK


class UserPublicationList(APITestCase):
    IMAGE_PATH = 'test.jpg'
    TEST_IMAGE = SimpleUploadedFile(name='test.jpg', content=open(IMAGE_PATH, 'rb').read(), content_type='image/jpeg');

    def setUp(self):
        test_user = User.objects.create(username='test', email='email@test.com')
        test_user.set_password('password')
        test_user.save()
        test_user_social_auth = UserSocialAuth.objects.create(user=test_user, provider='facebook', uid='10153580114080777')
        test_user_social_auth.save()
        test_publication = Publication.objects.create(text="Test title 1", author=test_user, image=self.TEST_IMAGE)
        test_publication.save()

    def test_get_ok(self):
        client = APIClient()
        test_user = User.objects.get(username='test')
        client.force_authenticate(test_user)
        response = client.get(USERS_PATH + str(test_user.pk) + '/publications/?cursor=')
        print response
        assert response.status_code == status.HTTP_200_OK
