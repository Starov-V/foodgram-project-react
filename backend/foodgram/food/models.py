from django.db import models
from users.models import User
from django.core.validators import RegexValidator, MinValueValidator

class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
        unique=True,
        validators=[RegexValidator(regex='^[A-Za-z]?'), ]
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        default="#ffffff",
        unique=True,
        validators=[RegexValidator(regex='^[#][0-9a-f]{6}?'), ]
    )
    slug = models.CharField(
        verbose_name='Идентификатор',
        max_length=7,
        unique=True
    )


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
    )
    measurement_unit = models.CharField(
        max_length=3
    )


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        through='TagRecipe'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    name = models.CharField(
        max_length=100
    )
    image = models.ImageField(
        upload_to='food/',
        blank=True,
    )
    text = models.CharField(
        max_length=100
    )
    is_favorited = models.BooleanField(
        default=False
    )
    is_in_shopping_cart = models.BooleanField(
        default=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(limit_value=1),]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        ordering = ['-pub_date']

class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()


class IsFavorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorites'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorites'
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]


class IsInCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        related_name='shopping_cart'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='shopping_cart'
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_in_cart'
            )
        ]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        default=None,
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            )
        ]