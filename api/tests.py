from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status


class FacebookAuthTests(APITestCase):

    FACEBOOK_TEST_TOKEN = 'EAAPuW6zXf0gBAEZAYrhhgp6OWma7OzX3stV3haylagwgNadgL9' \
                          'Ii0I6EsffzZACroOYl53lNBh996ZAt85usz4bhgTDiVbjA79pIVpgv31I37mZCtGJPz' \
                          'BvC6yDqke513f78BedyURikO71useBPK57KAwDyTaAPifoIeBxyqZCm1GSiIKDLU'

    FACEBOOK_TEST_USERNAME = 'OpenGraphTestUser'


    def test_auth_ok(self):

        """
        Ensure we can access with Facebook token
        """
        url = '/api/v0/me/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer facebook ' + self.FACEBOOK_TEST_TOKEN)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '"' + self.FACEBOOK_TEST_USERNAME + '"')


    def test_auth_error(self):
        """
        Ensure we can NOT access with INVALID Facebook token
        """
        url = '/api/v0/me/'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer facebook fake-ass-token')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

