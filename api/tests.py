from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

ROOT_PATH = '/api/v0'
ME_PATH = ROOT_PATH + '/me/'


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