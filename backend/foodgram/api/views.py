from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .pagination import CustomPagination
from django.db.models import Exists, OuterRef
from users.models import User
from django.http import HttpResponse
from food.models import Tag, Ingredient, Recipe, IsFavorite, IsInCart, Follow, IngredientRecipe
from .serializers import (IngredientRecipe, GetIngredientSerializer, FollowSerializer,
                          TagSerializer, CreateRecipeSerializer,  IsInCartSerializer, 
                          IsFavoriteSerializer, UserSerializer, PasswordSerializer,
                          FollowShowSerializer)
from .permissions import IsAuthor
from .filters import IngredientFilter, RecipeFilter


class PasswordView(APIView):
        serializer_class = PasswordSerializer
        queryset = User.objects.all()
        permission_classes = (IsAuthenticated,)



        def post(self, request, *args, **kwargs):
            self.object = self.request.user
            serializer = PasswordSerializer(data=request.data)

            if serializer.is_valid():
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return HttpResponse(status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend,)


    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)


class GetIngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = GetIngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = CreateRecipeSerializer
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if (self.action == 'update'):
            return (IsAuthor(), )
        elif self.action == 'destroy':
            return (IsAuthor(), )
        elif self.action == 'create':
            return (IsAuthenticated(), )
        else:
            return (AllowAny(), )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            'ingredients', 'tags'
        ).annotate(
            favorite=Exists(
                IsFavorite.objects.filter(
                    user=self.request.user, recipe=OuterRef('id')
                )
            ),
            shopping_cart=Exists(
                IsInCart.objects.filter(
                    user=self.request.user, recipe=OuterRef('id')
                )
            )
        )


class IsFavoriteViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    serializer_class = IsFavoriteSerializer
    queryset = IsFavorite.objects.all()
    pagination_class = None
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        recipe = Recipe.objects.filter(id=self.kwargs.get('recipe_id')).get()
        user = self.request.user
        if serializer.is_valid():
            serializer.save(
                recipe=recipe,
                user=user)

    @action(methods=['delete'], detail=True)
    def delete(self, request, recipe_id=None):
        user = request.user
        recipe = Recipe.objects.filter(id=recipe_id).get()
        obj = IsFavorite.objects.filter(recipe=recipe, user=user)
        obj.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

class IsInCartViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = IsInCartSerializer
    queryset = IsInCart.objects.all()
    pagination_class = None
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        recipe = Recipe.objects.filter(id=self.kwargs.get('recipe_id')).get()
        user = self.request.user
        if serializer.is_valid():
            serializer.save(
                recipe=recipe,
                user=user)
  
    @action(methods=['delete'], detail=True)
    def delete(self, request, recipe_id=None):
        user = request.user
        recipe = Recipe.objects.filter(id=recipe_id).get()
        obj = IsInCart.objects.filter(recipe=recipe, user=user)
        obj.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    def download_list(self, request):
        recipes = IsInCart.objects.filter(user_id=request.user)
        ingredient_dict = {}
        ingredients_list = []

        for recipe in recipes:
            ingredients_list.append(
                IngredientRecipe.objects.
                filter(recipe=recipe.recipe)
                .values_list('ingredient__name','ingredient__measurement_unit', 'amount')
            )

        for recipe in ingredients_list:
            for ingredient in recipe:
                key = ingredient[0] + ' (' + ingredient[1] + ') - '
                if key in ingredient_dict:
                    ingredient_dict[key] += ingredient[2]
                else:
                    ingredient_dict[key] = ingredient[2]

        filename = 'shopping_list.txt'
        file_list = []
        for key, value in ingredient_dict.items():
            file_list.append(key + ' ' + str(value))
        file = HttpResponse(
            'Список покупок: \n' + '\n'.join(file_list),
            content_type='text/plain'
        )
        file['Content-Disposition'] = (f'attachment; filename={filename}')
        return file


class FollowViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        if serializer.is_valid():
            
            serializer.save(
                user=self.request.user,
                following=User.objects.filter(id=self.kwargs.get('user_id')).get()
            )

    @action(methods=['delete'], detail=True)
    def delete(self, request, user_id=None):
        user = request.user
        following = User.objects.filter(id=user_id).get()
        obj = Follow.objects.filter(following=following, user=user)
        obj.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ShowFollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowShowSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination
    queryset = User.objects.all()

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowShowSerializer(page, many=True,
                                             context={'request': request})
        return self.get_paginated_response(serializer.data)
