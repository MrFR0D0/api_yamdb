from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


class UserAdmin(BaseUserAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role',
        'confirmation_code'
    )

    list_editable = ('role',)


admin.site.register(User, UserAdmin)
