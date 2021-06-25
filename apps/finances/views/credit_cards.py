"""Credit card views"""


# Django Rest Framework
from rest_framework import viewsets, mixins

# Models
from apps.finances.models import CreditCard

# Serializers
from apps.finances.serializers import CreditCardModelSerializer


class CreditCardViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ Credit card query views set"""

    serializer_class = CreditCardModelSerializer
    queryset = CreditCard.objects.all()
