from rest_framework import permissions


class IsAdminOrStaff(permissions.BasePermission):
    """Класс определяющий права доступа.

    Для аутентифицированных пользователей имеющих статус администратора.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Класс определяющий права доступа.

    Для аутентифицированных пользователей имеющих статус администратора
    или только чтение.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Класс определяющий права доступа.

    Для аутентифицированных пользователей имеющих статус администратора
    или автора записи или только чтение.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
