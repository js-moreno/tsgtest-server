"""User views"""


# Django Rest Framework
from rest_framework import viewsets

# Models
from apps.accounts.models import User

# Serializers
from apps.accounts.serializers import UserModelSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ User query views set"""

    serializer_class = UserModelSerializer
    queryset = User.objects.all()
