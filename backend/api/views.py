from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from users.models import User
from recipes.models import Tag, Recipe, Favorite, Shopping_cart, IngredientInRecipe, Ingredient 
from .serializers import IngredientSerializer, TagSerializer, RecipeGetSerializer, FavoriteSerializer
from .serializers import RecipePostSerializer, RecipeShortSerializer, ShoppingCartSerializer

from django.db.models import F, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets, serializers
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilter, IngredientFilter
from .permissions import IsAuthorOrAdminOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated
from .pagination import CustomPagination
from .utils import post_and_delete_action



class RecipeShortSerializer(serializers.ModelSerializer):
    '''Сериализатор для отображения рецептов при запросе подписок''' 

    class Meta: 
        model = Recipe
        fields = (
            'id',            
            'name',
            'image',             
            'cooking_time'
        )
    

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт  api/ingredients/.
    GET запрос: Получение списка всех ингредиентов с
    возможностью поиска по name.
    Эндпоинт  api/ingredients/id.
    GET запрос: получение ингредиента по id
    Права доступа: Доступно без токена.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт  api/tags/.
    GET запрос: Получение списка всех тэгов
    Эндпоинт  api/tags/id.
    GET запрос: получение тэгов по id
    Права доступа: Доступно без токена.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Эндпоинт  api/recipes/.
    GET запрос: Получение списка всех рецептов.
    Страница доступна всем пользователям. Пагинация.
    Доступна фильтрация по избранному, автору, списку покупок и тегам.

    POST запрос: Создать рецепт. Доступно только авторизованному пользователю.    

    Эндпоинт  api/recipes/id.
    GET запрос: получение рецепта по id. Доступно только авторизованным.
    PATCH и DELETE запрос доступно только автору рецепта.

    Эндпоинт  api/recipes/favorite.
    POST и DEL запрос: создание и удаление подписки.
    Доступно только авторизованному.

    Эндпоинт api/recipes/download_shopping_cart
    GET запрос: скачать список покупок.
    """
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        elif self.action in ['favorite', 'shopping_cart', ]:
            return RecipeShortSerializer

        return RecipePostSerializer

    def get_queryset(self):

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None and int(is_favorited) == 1:
            return Recipe.objects.filter(
                FavoriteRecipe__user=self.request.user
            )
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        if is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            return Recipe.objects.filter(shopping_cart__user=self.request.user)

        return Recipe.objects.all()


    @action(["POST", "DELETE"], detail=True)
    def favorite(self, request, **kwargs):
        return post_and_delete_action(
            self, request, Recipe, Favorite, FavoriteSerializer, **kwargs
        )

    @action(["POST", "DELETE"], detail=True)
    def shopping_cart(self, request, **kwargs):
        return post_and_delete_action(
            self, request, Recipe, Shopping_cart, ShoppingCartSerializer, **kwargs
        )

    @action(
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        user = request.user        
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=user).values(
            name=F('ingredient__name'),
            measurement_unit=F('ingredient__measurement_unit')).annotate(
            amount=Sum('amount')
        )
        
        data = []
        for ingredient in ingredients:
            data.append(
                f'{ingredient["name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["measurement_unit"]}'
            )
        content = 'Список покупок:\n\n' + '\n'.join(data)
        filename = 'Shopping_cart.txt'        
        request = HttpResponse(content, content_type='text/plain')
        request['Content-Disposition'] = f'attachment; filename={filename}'
        return request

