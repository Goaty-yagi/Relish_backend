from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "UID",
            "username",
            "avatar",
            "is_active",
        ]


class CustomUserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = DjoserUserSerializer.Meta.model
        fields = (
            "UID",
            "username",
            "avatar",
            "is_active"
        )
