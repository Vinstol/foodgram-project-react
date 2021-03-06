from django.urls import include, path
from recipes.views import IngredientsViewSet, RecipeViewSet, TagsViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]
