from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipes.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipes:ingredients-list')


class PublicIngredientAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()  # Define client user
    
    def test_login_required(self):
        """Test login required to access endpoint"""
        response = self.client.get(INGREDIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(email="test@gmail.com", password="testpassword")
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test to obtain list of all existent ingredients"""
        Ingredient.objects.create(user=self.user, name="Potato")
        Ingredient.objects.create(user=self.user, name="Vinegar")

        response = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_limited_to_user(self):
        """Test return only the ingredients from the authenticated user"""
        user2 = get_user_model().objects.create_user(email="test2@gmail.com", password="testpassword")

        Ingredient.objects.create(user=user2, name="Vinegar")

        ingredient_user_1 = Ingredient.objects.create(user=self.user, name="Apple")
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], ingredient_user_1.name)
    
    def test_create_ingredient_successful(self):
        """Test to create new ingredient"""
        payload = {'name': 'Chocolate'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(user=self.user, name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        payload = {'name': ''}
        response = self.client.post(INGREDIENTS_URL, payload)

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)