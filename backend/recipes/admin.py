from django.contrib import admin

from .models import Recipe, Tag, IngredientInRecipe, Shopping_cart, Favorite, Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка отображения данных о рецептах
    в интерфейсе администратора.
    """

    list_display = ('pk', 'author', 'name',)
    list_filter = ('author', 'name')
    filter_horizontal = ('ingredients',)


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


#@admin.register(TagRecipe)
#class TagRecipeAdmin(admin.ModelAdmin):
#    """Настройки отображения данных о тэгах привязанных к рецепту
#    в интерфейсе администратора.
#    """
#    list_display = ('tag', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Настройки отображения данных о рецептах, которые пользователи отмечают избранными.
    """
    list_display = ('user', 'recipe')


@admin.register(Shopping_cart)
class Shopping_cartAdmin(admin.ModelAdmin):
    """Настройки отображения списка покупок."""

    list_display = ('user', 'recipe')
