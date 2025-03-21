from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """Функция получения токена для пользователя."""
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
    }
