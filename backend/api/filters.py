import django_filters
from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(django_filters.FilterSet):
    """Фильтр для ингредиентов."""
    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтр для рцептов."""
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="slug",
    )
    author = django_filters.ModelMultipleChoiceFilter(
        queryset=Recipe.objects.all(),
        field_name="author__id",
        to_field_name="id",
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
