from django.contrib import admin

from .models import (Recipe, Tag, IngredientInRecipe,
                     ShoppingCart, Favorite, Ingredient)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка отображения данных о рецептах
    в интерфейсе администратора.
    """
    list_display = ('name', 'author', 'pub_date', 'display_tags', 'favorite')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name',)
    readonly_fields = ('favorite',)
    fields = ('image',
              ('name', 'author'),
              'text',
              ('tags', 'cooking_time'),
              'favorite')

    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Теги'

    def favorite(self, obj):
        return obj.favorite.count()
    favorite.short_description = 'Раз в избранном'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройки отображения данных о тэгах
    в интерфейсе администратора.
    """
    list_display = ('pk', 'name', 'slug', 'color',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка отображения данных об ингредиентах
    в интерфейсе администратора.
    """
    list_display = ('pk', 'name', 'measurement_unit')


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    """Настройки отображения данных об ингредиентах в рецептах
    в интерфейсе администратора.
    """
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Настройки отображения данных о рецептах,
    которые пользователи отмечают избранными.
    """
    list_display = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Настройки отображения списка покупок."""

    list_display = ('user', 'recipe')
