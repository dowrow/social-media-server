import json

from api.models import Publication
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

ROOT_PATH = '/api/v0'
ME_PATH = ROOT_PATH + '/me/'
PUBLICATIONS_PATH = ROOT_PATH + '/publications/'


class MeTests(APITestCase):
    def setUp(self):
        test_user = User.objects.create(username='test', email='email@test.com')
        test_user.set_password('password')
        test_user.save()

    @staticmethod
    def test_get_fail():
        client = APIClient()
        response = client.get(ME_PATH)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        client.logout()

    @staticmethod
    def test_get_ok():
        client = APIClient()
        test_user = User.objects.get(username='test')
        client.force_authenticate(test_user)
        response = client.get(ME_PATH)
        assert response.status_code == status.HTTP_200_OK

    @staticmethod
    def test_delete():
        client = APIClient()
        test_user = User.objects.get(username='test')
        client.force_authenticate(test_user)
        response = client.delete(ME_PATH)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.filter(username='test').exists() == False


class PublicationTests(APITestCase):
    IMAGE_PATH = 'test.jpg'
    TEST_IMAGE = SimpleUploadedFile(name='test.jpg', content=open(IMAGE_PATH, 'rb').read(), content_type='image/jpeg');

    def setUp(self):
        test_user = User.objects.create(username='test', email='email@test.com')
        test_user.set_password('password')
        test_user.save()
        test_user2 = User.objects.create(username='test2', email='email2@test.com')
        test_user2.set_password('password2')
        test_user2.save()
        test_publication = Publication.objects.create(text="Test title 1", author=test_user, image=self.TEST_IMAGE)
        test_publication2 = Publication.objects.create(text="Test title 2", author=test_user2, image=self.TEST_IMAGE)
        test_publication.save()
        test_publication2.save()

    def test_get_ok(self):
        client = APIClient()
        test_user = User.objects.get(username='test')
        client.force_authenticate(test_user)
        response = client.get(PUBLICATIONS_PATH)
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
        assert response.status_code == status.HTTP_204_NO_CONTENT
