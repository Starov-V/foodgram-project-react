from rest_framework import serializers
from users.models import User
from users.validators import validate_username
from food.models import Tag, Ingredient, Recipe, IngredientRecipe, IsFavorite, IsInCart, Follow
from .mixins import UsernameValidationMixin
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.validators import UniqueTogetherValidator
import io



class UserSerializer(UserCreateSerializer):
    is_follow = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_follow',
            'password'
        )
    def get_is_follow(self, obj):
        if not self.context.get('request').user.is_authenticated:
            return 0
        user = self.context.get('request').user
        if Follow.objects.filter(user=user, following=obj):
            return 1
        else:
            return 0

class PasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('current_password', 'new_password')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientRecipeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit_id')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)
    


class GetIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IsFavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        read_only=True, slug_field='name',
        default=1
    )
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    def create_serializer_object(self, request, pk):
        user = request.user
        recipe = Recipe.objects.filter(id=pk)
        IsFavorite.objects.create(user=user, recipe=recipe)

    class Meta:
        model = IsFavorite
        fields = (
            'recipe',
            'user'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=IsFavorite.objects.all(),
                fields=['user', 'recipe'],
            )
        ]


class IsInCartSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        read_only=True, slug_field='name',
        default=1
    )
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = IsInCart
        fields = (
            'recipe',
            'user'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=IsInCart.objects.all(),
                fields=['user', 'recipe'],
            )
        ]

class ImageConversion(serializers.Field):
    def to_representation(self, value):
        if value:
            return value
        else:
            return None

    def to_internal_value(self, data):
        try:
            if not data:
                decode = io.BytesIO(io.base64.b64decode(data))
                image = io.Image.open(decode)
            else:
                return 0
        except ValueError:
            raise serializers.ValidationError(
                'Картинка должна быть кодирована в base64'
            )
        return image

class RecipeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        read_only=True,
        many=True,
        source='ingredientrecipe_set'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = ImageConversion()
        
    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        if not self.context.get('request').user.is_authenticated:
            return 0
        user = self.context.get('request').user
        if IsFavorite.objects.filter(recipe=obj.id, user=user):
            return 1
        else:
            return 0

    def get_is_in_shopping_cart(self, obj):
        if not self.context.get('request').user.is_authenticated:
            return 0
        user = self.context.get('request').user
        if IsInCart.objects.filter(recipe=obj.id, user=user):
            return 1
        else:
            return 0


class CreateRecipeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def ingredients_create_update(self, ingredients, recipe):
        updated_list = []
        to_delete_list = []
        for ingredient in ingredients:
            if not IngredientRecipe.objects.filter(ingredient=ingredient['id'], recipe=recipe):
                updated_list.append(ingredient)
            else:
                to_delete_list.append(ingredient)
        if not to_delete_list:
            ingredients_list = [
                IngredientRecipe(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(id=ingredient['id']),
                    amount=ingredient['amount'],
                ) for ingredient in updated_list
            ]
            IngredientRecipe.objects.bulk_create(ingredients_list)
        else:
            for ingredient in to_delete_list:
                IngredientRecipe.objects.filter(ingredient=ingredient['id'], recipe=recipe).delete()

    def create(self, validated_data):
        ingredients = self.initial_data.get('ingredients')
        validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.ingredients_create_update(
            ingredients=ingredients,
            recipe=recipe
        )
        return recipe
    def update(self, instance, validated_data):
        tags = validated_data.get('tags', instance.tags)
        instance.tags.set(tags)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        ingredients = self.initial_data.get('ingredients')
        self.ingredients_create_update(
            ingredients=ingredients,
            recipe=Recipe.objects.get(id=instance.id),
        )
        return instance
    def to_representation(self, instance):
        return RecipeSerializer(
            instance=instance, context=self.context).data


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        #default=serializers.CurrentUserDefault()
    )

    class Meta:
        """Мета-класс для сериализатора для подписок."""

        fields = (
            'user',
            'following'
        )
        read_only_fields = ('user', )
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError
        return data
