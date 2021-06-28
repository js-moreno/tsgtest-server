"""Credit card serializer"""

# Django
from django.utils.translation import gettext_lazy as _


# Django Rest Framework
from rest_framework import serializers

# Models
from apps.finances.models import CreditCard


class CreditCardModelSerializer(serializers.ModelSerializer):
    """Credit card model serializer"""

    number = serializers.CharField(write_only=True)
    verification_code = serializers.CharField(write_only=True)
    truncated_number = serializers.ReadOnlyField()
    due_date = serializers.ReadOnlyField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    customer = serializers.ReadOnlyField()

    class Meta:
        model = CreditCard
        fields = "__all__"

    def validate_number(self, value):
        if not value.isnumeric():
            raise serializers.ValidationError(_("You only can use numbers as credit card number"))
        if len(value) > 19 or len(value) < 16:
            raise serializers.ValidationError(
                _("Your credit card number must be between 16 and 19 digits")
            )
        return value

    def validate_verification_code(self, value):
        if not value.isnumeric():
            raise serializers.ValidationError(_("You only can use numbers as verification code"))
        if len(value) > 4 or len(value) < 3:
            raise serializers.ValidationError(
                _("Your verification code must be between 3 and 4 digits")
            )
        return value


class CreditCardSuperUserModelSerializer(serializers.ModelSerializer):
    """Credit card model serializer to super users"""

    number = serializers.CharField(write_only=True)
    verification_code = serializers.CharField(write_only=True)
    truncated_number = serializers.ReadOnlyField()
    due_date = serializers.ReadOnlyField()
    customer = serializers.ReadOnlyField()

    class Meta:
        model = CreditCard
        fields = "__all__"

    def validate_number(self, value):
        if not value.isnumeric():
            raise serializers.ValidationError(_("The credit card number must contain only numbers"))
        if len(value) > 19 or len(value) < 16:
            raise serializers.ValidationError(
                _("The credit card number must be between 16 and 19 digits")
            )
        return value

    def validate_verification_code(self, value):
        if not value.isnumeric():
            raise serializers.ValidationError(_("The verification code must contain only numbers"))
        if len(value) > 4 or len(value) < 3:
            raise serializers.ValidationError(
                _("The verification code must be between 3 and 4 digits")
            )
        return value
