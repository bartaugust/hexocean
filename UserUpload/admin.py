from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserTier


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'tier')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2','tier'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserTier)
