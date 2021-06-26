"""Credit card views"""


# Django Rest Framework
from rest_framework import viewsets, mixins

# Models
from apps.finances.models import CreditCard

# Serializers
from apps.finances.serializers import CreditCardModelSerializer, CreditCardSuperUserModelSerializer


class CreditCardViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """ Credit card query views set"""

    serializer_class = CreditCardModelSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CreditCard.objects.all()
        return CreditCard.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return CreditCardSuperUserModelSerializer
        return CreditCardModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)