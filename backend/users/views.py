from django.contrib.auth import update_session_auth_hash
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.serializers import SetPasswordSerializer


from .serializers import (UserGetSerializer, UserPostSerializer,
                          SubscriptionSerializer, UserWithRecipesSerializer)
from .models import User, Subscription
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.pagination import CustomPagination
from api.utils import post_and_delete_action


class CustomUserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Управление пользователями и подписками.
    Эндпоинты:
    /api/users/
    GET запрос: полусить список всех зарегистрированных пользователей
    Подключена пагинация.
    POST запрос: создать нового пользователя. Доступно всем.

    /api/users/{id}
    GET запрос: профиля пользователя. Доступно только авторизованным.

    /api/users/me
    GET запрос: профиль текущего пользователя. Доступно только авторизованным.

    /api/users/set_password/
    POST запрос: смена пароля. Доступно только авторизованным.

    /api/users/subscriptions/
    GET запрос: Возвращает пользователей, на которых
    подписан текущий пользователь.
    Только авторизованным. В выдачу подключены рецепты с возможностью
    установить лимит на их колличество.

    /api/users/{id}/subscribe/
    POST запрос: подписаться на пользователя. Только авторизованным.
    DELETE запрос: отписаться от пользователя.
    """

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

        self.request.user.set_password(serializer.data["new_password"])
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
                users, many=True,  context={'request': request})

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
        