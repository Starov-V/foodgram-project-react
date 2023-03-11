from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from .views import  TagViewSet, RecipeViewSet, GetIngredientViewSet, IsFavoriteViewSet, IsInCartViewSet, FollowViewSet, UsersViewSet

v1_router = routers.DefaultRouter()

v1_router.register('tags', TagViewSet)
v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('ingredients', GetIngredientViewSet)
#v1_router.register('users', UsersViewSet.as_view({'get':'list'}), basename='users')

v1_router.register(r'recipes/(?P<recipe_id>\d+)/favorite', IsFavoriteViewSet)
v1_router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', IsInCartViewSet)
v1_router.register(r'users/(?P<user_id>\d+)/subscribe', FollowViewSet, basename='follows')

urlpatterns = [
    
    #path('users/', SignUpView.as_view(), name='sign_up'),
    #path('auth/token/login/', views.obtain_auth_token),
    #path('auth/token/logout/', views.obtain_auth_token),
    #path('users/set_password/', PasswordView.as_view(), name='set_password'),
    #path('users/', user_create, name='create'),
    #path('users/', UsersViewSet, name='list'),
    #path(r'users/(?P<user_id>\d+)/', user_detail, name='detail'),
    #path('users', UsersViewSet.as_view({'get':'list'})),
    path(r'recipes/download_shopping_cart/', IsInCartViewSet.as_view({'get':'download_list'})),
    #path(r'users/(?P<user_id>\d+)/subscribe/', FollowViewSet.as_view({'delete':'destroy'})),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    
]
