from rest_framework import serializers

from .models import Award, BaseAward


class BaseAwardSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseAward
        fields = "__all__"


class AwardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Award
        fields = "__all__"
