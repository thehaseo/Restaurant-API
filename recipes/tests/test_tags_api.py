from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipes.serializers import TagSerializer


TAGS_URL = reverse('recipes:tags-list')

class PublicTagsAPITests(TestCase):
    """Test tag status delivered to public users without authentication"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """If user is not authenticated it should not be able to retrieve tags info"""
        response = self.client.get(TAGS_URL)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('test@gmail.com', 'testpassword')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name='Chicken')
        Tag.objects.create(user=self.user, name='Meat')

        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test the tags returned belongs to the authenticated user"""
        user2 = get_user_model().objects.create_user('testuser2@gmail.com', 'testpassword2')
        Tag.objects.create(user=user2, name='Chicken')
        tag = Tag.objects.create(user=self.user, name='Meat')
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test tag creation when sending correct parameters in POST method"""
        payload = {'name': 'Simple'}
        
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(user=self.user, name=payload['name']).exists()
        
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        payload = {'name': ''}
        response = self.client.post(TAGS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)