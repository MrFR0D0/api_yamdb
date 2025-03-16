import re

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api_yamdb import constants


def username_validator(value):
    """Функция для проверка имени пользователя."""
    regex = constants.USERNAME_CHECK
    if re.search(regex, value) is None:
        invalid_characters = set(re.findall(r'[^\w.@+-]', value))
        raise ValidationError(
            (
                f'Не допустимые символы {invalid_characters} в username. '
                'username может содержать только буквы, цифры и '
                'знаки @/./+/-/_.'
            ),
        )

    if value == settings.NOT_ALLOWED_USERNAME:
        raise ValidationError(
            f'Использовать имя   "{settings.NOT_ALLOWED_USERNAME}" в качестве '
            'username запрещено.',
        )


def validate_username(username):
    """Функция для проверка имени пользователя."""
    if username == settings.NOT_ALLOWED_USERNAME:
        raise serializers.ValidationError(
            f'Имя "{settings.NOT_ALLOWED_USERNAME}" для username запрещено.',
        )
    return username
