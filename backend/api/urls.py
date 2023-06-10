from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, TagViewSet,
                    RecipeViewSet, SubscriptionsView, FollowUserView)

app_name = 'api'

router = DefaultRouter()

# router.register('users', CustomUserViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('users/subscriptions/', SubscriptionsView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('users/<int:id>/subscribe/', FollowUserView.as_view()),
]
