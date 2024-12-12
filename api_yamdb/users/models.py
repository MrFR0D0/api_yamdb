from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb import constants


class User(AbstractUser):
    """Модель пользователя."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOICES = (
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    )
    role = models.CharField(
        max_length=constants.MAX_ROLE_LENGHT,
        choices=CHOICES,
        default=USER,
        verbose_name='Уровень доступа пользователя',
        help_text='Уровень доступа пользователя'
    )

    bio = models.TextField(
        max_length=constants.MAX_BIO_LENGHT,
        blank=True,
        verbose_name='Заметка о пользователе',
        help_text='Напишите заметку о себе'
    )

    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта пользователя',
        help_text='Введите свой электронный адрес'
    )

    confirmation_code = models.CharField(
        blank=True,
        verbose_name='Код для авторизации',
        max_length=constants.MAX_CONFCODE_LENGHT,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            ),
        )

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff


User = get_user_model()
