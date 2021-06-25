"""Accounts admin"""

# Django
from django.contrib import admin


# Models
from apps.finances.models import CreditCard


admin.site.register(CreditCard)
