from django.contrib.auth.models import UserManager

from django.conf import settings


class UserManager(UserManager):
    """Сохраняет пользователя только с email."""

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле email обязательное')
        if username == settings.NOT_ALLOWED_USERNAME:
            raise ValueError(
                'Использование имени пользователя '
                f'{settings.NOT_ALLOWED_USERNAME} запрещено!'
            )
        return super().create_user(
            username, email=email, password=password, **extra_fields)

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)
