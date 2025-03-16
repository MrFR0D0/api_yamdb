from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User

ADDITIONAL_USER_FIELDS = (
    (None, {'fields': ('some_additional_field',)}),
)


class UserAdmin(BaseUserAdmin):
    """Класс администрирования пользователя."""

    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role',
        # 'confirmation_code',
    )

    list_editable = ('role',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'Personal info',
            {'fields': ('first_name', 'last_name', 'email', 'bio')},
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active', 'is_staff',
                    'is_superuser', 'groups', 'user_permissions',
                ),
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('role', 'confirmation_code')}),
    )

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'username', 'email', 'first_name', 'last_name',
                    'password', 'bio', 'role', 'confirmation_code',
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
