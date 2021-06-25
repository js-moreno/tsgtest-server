"""Credit card serializer"""


# Django Rest Framework
from rest_framework import serializers

# Models
from apps.finances.models import CreditCard


class CreditCardModelSerializer(serializers.ModelSerializer):
    """Credit card model serializer"""

    class Meta:
        model = CreditCard
        fields = "__all__"