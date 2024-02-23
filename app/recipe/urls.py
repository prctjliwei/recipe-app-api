"""
URL mappings for the recipe API
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register(prefix='recipes', viewset=views.RecipeViewSet)
router.register(prefix='tags', viewset=views.TagViewSet)
router.register(prefix='ingredients', viewset=views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
