# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DocumentationConfig(AppConfig):
    name = "documentation"
    verbose_name = _("Documentation")
