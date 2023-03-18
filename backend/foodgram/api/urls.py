from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from .views import  TagViewSet, RecipeViewSet, GetIngredientViewSet, IsFavoriteViewSet, IsInCartViewSet, FollowViewSet, UsersViewSet

v1_router = routers.DefaultRouter()

v1_router.register('tags', TagViewSet)
v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('ingredients', GetIngredientViewSet)
v1_router.register(r'recipes/(?P<recipe_id>\d+)/favorite', IsFavoriteViewSet)
v1_router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', IsInCartViewSet)
v1_router.register(r'users/(?P<user_id>\d+)/subscribe', FollowViewSet, basename='follows')

urlpatterns = [
    path(r'recipes/download_shopping_cart/', IsInCartViewSet.as_view({'get':'download_list'})),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    
]
