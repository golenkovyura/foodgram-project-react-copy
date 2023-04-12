from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, TagViewSet, RecipeViewSet
from users.views import CustomUserViewSet


app_name = 'api'

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path(r'', include(router.urls)),    
    path(r'auth/', include('djoser.urls.authtoken')),       
]
