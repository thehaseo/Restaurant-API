from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipes.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipes:recipes-list')

def sample_tag(user, name="spicy"):
    """Creates example tag"""
    return Tag.objects.create(user=user, name=name)

def sample_ingredient(user, name='Cinnamon'):
    return Ingredient.objects.create(user=user, name=name)

def detail_url(recipe_id):
    return reverse('recipes:recipes-detail', args=[recipe_id])

def sample_recipe(user, **params):
    defaults = {
        "title": "Sampe recipe",
        "time_minutes": 10,
        "price": 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """Test to retrieve all recipes for authenticated user"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(email='test@gmail.com', password='testpassword')
        self.client.force_authenticate(self.user)
    
    def test_retrieve_all_recipes(self):
        sample_recipe(self.user)
        sample_recipe(self.user)

        response = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recipes_limited_to_user(self):
        user2 = get_user_model().objects.create_user('test2@gmail.com', 'testpassword')
        
        sample_recipe(user=self.user)
        sample_recipe(user=user2)

        response = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    def test_view_recipe_detail(self):
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        response = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(response.data, serializer.data)

    def test_create_basic_recipe(self):
        payload = {
            'title': "Test recipe",
            'time_minutes': 30,
            'price': 10.00
        }
        response = self.client.post(RECIPES_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=response.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        tag1 = sample_tag(user=self.user, name="Tag 1")
        tag2 = sample_tag(user=self.user, name="Tag 2")
        payload = {
            'title': "Test recipe",
            'tags': [tag1.id, tag2.id],
            'time_minutes': 30,
            'price': 10.00
        }
        response = self.client.post(RECIPES_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        recipe = Recipe.objects.get(id=response.data['id'])
        tags = recipe.tags.all()
        
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

        
        

    

