from django.contrib import admin
from recipes import models

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """Класс админимтрирования модели Tag."""

    list_display = ('id', 'name', 'slug')


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Класс админимтрирования модели Ingredient."""

    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ['name']
    search_fields = ('name',)


class RecipeIngredientsInline(admin.TabularInline):
    """Класс админимтрирования модели RecipeIngredients на странице Recipe."""

    model = models.RecipeIngredients
    min_num = 1
    extra = 1


class RecipeTagsInline(admin.TabularInline):
    """Класс админимтрирования модели RecipeTags на странице Recipe."""

    model = models.RecipeTags
    min_num = 1
    extra = 0


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Класс админимтрирования модели Recipe."""

    list_display = ('id', 'name', 'author', 'in_favorite')
    list_filter = ['name', 'author', 'tags']
    inlines = (RecipeIngredientsInline, RecipeTagsInline)

    def in_favorite(self, obj):
        return obj.in_favorite.all().count()


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Класс админимтрирования модели Favorite."""

    list_display = ('id', 'user', 'recipe')


@admin.register(models.ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Класс админимтрирования модели ShoppingList."""

    list_display = ('id', 'user', 'recipe')
