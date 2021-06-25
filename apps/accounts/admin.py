"""Accounts admin"""

# Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Models
from apps.accounts.models import User


class UserAdmin(BaseUserAdmin):
    """Custom admin model from django user admin model."""

    fieldsets = (
        (
            _("Personal information"),
            {"fields": ("first_name", "last_name", "email", "phone", "address")},
        ),
        (
            _("Account information"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "password1", "password2")}),
    )
    readonly_fields = ("last_login", "date_joined")
    list_display = ("email", "first_name", "last_name", "is_staff", "last_login")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
