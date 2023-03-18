from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username, validate_password


class User(AbstractUser):
    GUEST = 0
    AUTORIZED = 1
    ADMIN = 2

    ROLE_CHOICE = (
        (GUEST, 'guest'),
        (AUTORIZED, 'autorized'),
        (ADMIN, 'admin')

    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_username, ]
    )
    password = models.CharField(
        max_length=150,
        null=True,
        default=None,
        validators=[validate_password, ]

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
        default=GUEST
    )

    @property
    def is_admin(self):
        if self.role == 'admin':
            return True

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
