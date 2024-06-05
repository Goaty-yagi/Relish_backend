from rest_framework import serializers
from .models import AwardType


class AwardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardType
        fields = [
            "id",
            "name",
        ]
