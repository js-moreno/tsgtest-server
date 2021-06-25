"""Finances utils"""

# Django
from django.db.models import TextChoices
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class CreditCardFranchises(TextChoices):
    """Credit card available franchises"""

    VISA = "Visa"
    MASTERCARD = "MasterCard"
    AMERICAN_EXPRESS = "American Express"
    DINERS_CLUB = "Diners Club"


only_numbers = RegexValidator(r"^[\d]*$", _("You only can use numbers in this field"))