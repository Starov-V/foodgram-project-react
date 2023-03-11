from django.db import models
from users.models import User

class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        default="#ffffff",
        unique=True
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
        default=0
    )
    is_in_shopping_cart = models.BooleanField(
        default=0
    )
    cooking_time = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

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
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
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
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
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