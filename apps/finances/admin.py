"""Accounts admin"""

# Django
from django import forms
from django.contrib import admin
from django.utils.translation import gettext as _

# Models
from apps.finances.models import CreditCard


class CreditCardAdmin(admin.ModelAdmin):

    list_display = ("truncated_number", "franchise", "due_date", "customer", "is_principal")
    list_filter = ("franchise", "due_date_year", "due_date_month")
    search_fields = ("user__first_name", "user__last_name")

    def has_change_permission(self, request, obj=None):
        return False

    def get_fields(self, request, obj=None):
        fields = super(CreditCardAdmin, self).get_fields(request, obj)
        if obj:
            fields = ("truncated_number", "franchise", "due_date", "customer")
        return fields


admin.site.register(CreditCard, CreditCardAdmin)
