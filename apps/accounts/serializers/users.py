"""Users serializer"""


# Django Rest Framework
from rest_framework import serializers

# Models
from apps.accounts.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "password",
            "email",
            "phone",
            "address",
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data["password"])
            user.save()
        except KeyError:
            pass
        return user