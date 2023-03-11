from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username


class User(AbstractUser):
    ROLE_CHOICE = (
        ('autorized', 'autorized'),
        ('admin', 'admin')
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_username]
    )
    password = models.CharField(
        max_length=150,
        null=True,
        default=None
    )
    email = models.EmailField(
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICE,
        default='user'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
