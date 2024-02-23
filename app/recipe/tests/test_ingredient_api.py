"""Test ingredient APIs"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


def detail_url(ingred_id):
    """Ingredient detail url"""
    return reverse('recipe:ingredient-detail', args=[ingred_id])


def create_user(email='user@example.com', password='testpass123'):
    """create and return user"""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredientsApiTests(TestCase):
    """test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingredients"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name="kale")
        Ingredient.objects.create(user=self.user, name="Vanilla")

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_ingredients_limited_to_user(self):
        """test list of ingredients is limited to authenticated user"""
        user2 = create_user(email="otheruser@example.com")
        Ingredient.objects.create(user=user2, name='Salt')

        ingredient = Ingredient.objects.create(user=self.user, name='Curry')

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], ingredient.id)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_update_ingredient(self):
        ingredient = Ingredient.objects.create(name='Mistery', user=self.user)

        payload = {
            "name": "nah",
        }

        res = self.client.patch(detail_url(ingredient.id), payload, 'json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test deleting an ingredients"""
        ingredient = Ingredient.objects.create(name='Potato', user=self.user)

        res = self.client.delete(detail_url(ingredient.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exist = Ingredient.objects.filter(user=self.user).exists()

        self.assertFalse(exist)
