"""Credit card model"""

# Django
from django.db import models
import django.utils.timezone as timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)

# Django Cryptography
from django_cryptography.fields import encrypt

# Utils
from apps.finances.utils import CreditCardFranchises, only_numbers


class CreditCard(models.Model):
    """Model definition for credit cards"""

    number = encrypt(
        models.CharField(
            max_length=19,
            verbose_name=_("Number"),
            validators=[
                only_numbers,
                MinLengthValidator(16),
            ],
        )
    )
    franchise = models.CharField(
        max_length=255,
        verbose_name=_("Franchise"),
        choices=CreditCardFranchises.choices,
    )
    due_date_year = models.PositiveSmallIntegerField(
        _("Due date year"),
    )
    due_date_month = models.PositiveSmallIntegerField(
        _("Due date month"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ],
    )
    verification_code = encrypt(
        models.CharField(
            max_length=4,
            verbose_name=_("Verification code"),
            validators=[
                only_numbers,
                MinLengthValidator(3),
            ],
        )
    )
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, verbose_name=_("User"))

    @property
    def truncated_number(self):
        return "**********" + self.number[-4:]

    truncated_number.fget.short_description = _("Truncated number")

    @property
    def due_date(self):
        return str(self.due_date_month).zfill(2) + "/" + str(self.due_date_year)[-2:]

    due_date.fget.short_description = _("Due date")

    @property
    def customer(self):
        return str(self.user)

    customer.fget.short_description = _("Customer")

    class Meta:
        verbose_name = _("Credit card")
        verbose_name_plural = _("Credit cards")
