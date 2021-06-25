"""Credit card serializer"""


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

    class Meta:
        model = CreditCard
        fields = "__all__"