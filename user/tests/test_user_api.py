from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """Tests for interaction with user model for public clients without authentication"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            'email': 'testmeail@gmail.com',
            'password': 'testpass123',
            'name': 'Tester'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.payload)
        self.assertTrue(user.check_password())