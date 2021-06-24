"""Accounts admin"""

# Django
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Models
from apps.accounts.models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            "groups": forms.HiddenInput(),
            "user_permissions": forms.HiddenInput(),
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    """Custom admin model from django user admin model."""

    add_form = UserCreationForm

    fieldsets = (
        (_("Personal information"), {"fields": ("first_name", "last_name")}),
        (_("Account information"), {"fields": ("email", "is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("last_login", "date_joined")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff", "last_login")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
