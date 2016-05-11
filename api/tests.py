from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate, APIClient
from django.core.urlresolvers import reverse
from rest_framework import status

ROOT_PATH = '/api/v0'
LOGIN_PATH = ROOT_PATH + '/login/'


class LoginTests(APITestCase):

    def setUp(self):
        test_user = User.objects.create(username='test', email='email@test.com')
        test_user.set_password('password')
        test_user.save()

    def test_login_fail(self):
        client = APIClient()
        response = client.get(LOGIN_PATH)
        assert response.status_code == 401
        client.logout()

    def test_login_ok(self):
        client = APIClient()
        test_user = User.objects.get(username='test')
        client.force_authenticate(test_user)
        response = client.get(LOGIN_PATH)
        assert response.status_code == 200