from django.contrib.auth import update_session_auth_hash
from django.db.models import F, Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from djoser.serializers import SetPasswordSerializer

from recipes.models import (Tag, Recipe, Favorite,
                            ShoppingCart, IngredientInRecipe,
                            Ingredient)
from users.models import User, Subscription
from .serializers import (IngredientSerializer, TagSerializer,
                          RecipeGetSerializer, FavoriteSerializer,
                          RecipePostSerializer, RecipeShortSerializer,
                          ShoppingCartSerializer, UserGetSerializer,
                          UserPostSerializer, SubscriptionSerializer,
                          UserWithRecipesSerializer)
from .filters import RecipeFilter, IngredientFilter
from .permissions import IsAuthorOrAdminOrReadOnly
from .pagination import CustomPagination
from .utils import post_and_delete_action


class CustomUserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_instance(self):
        return self.request.user

    def get_serializer_class(self):

        if self.action in ['subscriptions', 'subscribe']:

            return UserWithRecipesSerializer

        elif self.request.method == 'GET':

            return UserGetSerializer

        elif self.request.method == 'POST':

            return UserPostSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, ]

        return super(self.__class__, self).get_permissions()

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance

        return self.retrieve(request, *args, **kwargs)

    @action(
        ["POST"],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()

        update_session_auth_hash(self.request, self.request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        users = User.objects.filter(
            following__user=request.user
        ).prefetch_related('recipes')
        page = self.paginate_queryset(users)

        if page is not None:
            serializer = UserWithRecipesSerializer(
                page, many=True,
                context={'request': request})

            return self.get_paginated_response(serializer.data)

        serializer = UserWithRecipesSerializer(
            users, many=True, context={'request': request}
        )

        return Response(serializer.data)

    @action(
        ["POST", "DELETE"],
        detail=True,
        permission_classes=[IsAuthorOrAdminOrReadOnly],
    )
    def subscribe(self, request, **kwargs):
        return post_and_delete_action(
            self, request, User, Subscription, SubscriptionSerializer, **kwargs
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
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт  api/tags/.
    GET запрос: Получение списка всех тэгов
    Эндпоинт  api/tags/id.
    GET запрос: получение тэгов по id
    Права доступа: Доступно без токена.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


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
    queryset = Recipe.objects.all()
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

    @action(["POST", "DELETE"], detail=True)
    def favorite(self, request, **kwargs):
        return post_and_delete_action(
            self,
            request,
            Recipe,
            Favorite,
            FavoriteSerializer,
            **kwargs
        )

    @action(["POST", "DELETE"], detail=True)
    def shopping_cart(self, request, **kwargs):
        return post_and_delete_action(
            self,
            request,
            Recipe,
            ShoppingCart,
            ShoppingCartSerializer,
            **kwargs
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
