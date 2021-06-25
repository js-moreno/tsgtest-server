"""Credit card model"""

# Django
from django.db import models
import django.utils.timezone as timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)

# Utils
from apps.finances.utils import CreditCardFranchises, only_numbers


class CreditCard(models.Model):
    """Model definition for credit cards"""

    number = models.CharField(
        max_length=19,
        verbose_name=_("Number"),
        validators=[
            only_numbers,
            MinLengthValidator(16),
        ],
    )
    franchise = models.CharField(
        max_length=255,
        verbose_name=_("Franchise"),
        choices=CreditCardFranchises.choices,
    )
    due_date_year = models.PositiveSmallIntegerField(
        _("Due date year"),
        validators=[
            MinValueValidator(timezone.now().year),
        ],
    )
    due_date_month = models.PositiveSmallIntegerField(
        _("Due date month"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ],
    )
    verification_code = models.PositiveBigIntegerField(
        verbose_name=_("Verification code"),
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(4),
        ],
    )
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, verbose_name=_("User"))

    class Meta:
        verbose_name = _("Credit card")
        verbose_name_plural = _("Credit cards")
