from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from .models import User, Subscription
from recipes.models import Recipe


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


class UserGetSerializer(UserSerializer):
    """Сериализатор для просмотра профиля пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:

            return False

        return Subscription.objects.filter(
            author=obj, user=request.user
            ).exists()


class UserWithRecipesSerializer(UserGetSerializer):
    """Сериализатор для просмотра пользователя с рецептами."""
    
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = UserGetSerializer.Meta.fields + (
            'recipes',
            'recipes_count'
        )       
    
    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, object):
        request = self.context.get('request')
        context = {'request': request}
        recipe_limit = request.query_params.get('recipe_limit')
        queryset = object.recipes.all()
        if recipe_limit:
            queryset = queryset[:int(recipe_limit)]

        return RecipeShortSerializer(queryset, context=context, many=True).data


class UserPostSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ('author', 'user', )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['author', 'user', ],
                message="Вы уже подписаны на этого пользователя"
            )
        ]

    def create(self, validated_data):
        return Subscription.objects.create(
            user=self.context.get('request').user, **validated_data)

    def validate_author(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                'Подписка на самого себя не возможна!')
        return value
