from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from foodgram.pagination import CustomPageNumberPaginator

from recipes.filters import IngredientsFilter, RecipeFilter
from recipes.models import (Ingredient, RecipeIngredients, Tag,
                     Recipe, Favorite, ShoppingList)
from recipes.serializers import (IngredientsSerializer, TagsSerializer,
                          ShowRecipeFullSerializer, AddRecipeSerializer,
                          FavouriteSerializer, ShoppingListSerializer)
from recipes.permissions import IsAuthorOrAdmin #, AdminOrAuthorOrReadOnly


class RetriveAndListViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass


class IngredientsViewSet(RetriveAndListViewSet):
    queryset = Ingredient.objects.all().order_by('id')
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None


class TagsViewSet(RetriveAndListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = ShowRecipeFullSerializer
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeFullSerializer
        return AddRecipeSerializer

    @action(detail=True, permission_classes=[IsAuthorOrAdmin])
    def favorite(self, request, pk):
        """Кастомный метод обработки эндпоинта ./favorite/."""
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavouriteSerializer(data=data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, id=pk)
        try:
            favorite = Favorite.objects.get(user=request.user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response(
                'Данный рецепт уже отсутствует в избранном.', 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, permission_classes=[IsAuthorOrAdmin])
    def shopping_cart(self, request, pk):
        """Кастомный метод обработки эндпоинта ./shopping_cart/."""
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingListSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            recipe = Recipe.objects.get(id=pk)
            shopping_list = ShoppingList.objects.get(user=request.user,
                                                     recipe=recipe)
            shopping_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Recipe.DoesNotExist:
            return Response(
                'Данный рецепт уже отсутствует в списке покупок.', 
                status=status.HTTP_400_BAD_REQUEST
            )
        except ShoppingList.DoesNotExist:
            return Response(
                'Данный рецепт уже отсутствует в списке покупок.', 
                status=status.HTTP_400_BAD_REQUEST
            )


    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        """Кастомный метод обработки эндпоинта ./download_shopping_cart/."""
        shopping_list = request.user.shopping_list.all()
        to_buy = get_ingredients_list(shopping_list)
        return download_response(to_buy, 'Список покупок.txt')


def get_ingredients_list(recipes_list):
    ingredients_dict = {}
    for recipe in recipes_list:
        ingredients = RecipeIngredients.objects.filter(recipe=recipe.recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in ingredients_dict:
                ingredients_dict[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                    }
            else:
                ingredients_dict[name]['amount'] += amount
    to_buy = []
    for item in ingredients_dict:
        to_buy.append(f'{item} - {ingredients_dict[item]["amount"]} '
                      f'{ingredients_dict[item]["measurement_unit"]} \n')
    return to_buy


def download_response(download_list, filename):
    response = HttpResponse(download_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
