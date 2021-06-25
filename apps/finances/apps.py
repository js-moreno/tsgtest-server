# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FinancesConfig(AppConfig):
    name = "apps.finances"
    verbose_name = _("Finances")