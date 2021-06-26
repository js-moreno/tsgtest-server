"""User views"""


# Django Rest Framework
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

# Drf-yasg
from drf_yasg.utils import swagger_auto_schema

# Models
from apps.accounts.models import User

# Serializers
from apps.accounts.serializers import UserModelSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ User query views set"""

    serializer_class = UserModelSerializer

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return User.objects.filter(pk=self.request.user.id)
        return User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(security=[])
    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request)
