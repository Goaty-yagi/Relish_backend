from rest_framework import serializers

from .models import Award, BaseAward


class BaseAwardSerializer(serializers.ModelSerializer):
    cuisine_type = serializers.CharField(source='cuisine_type.name', read_only=True)

    class Meta:
        model = BaseAward
        fields = [
            'id', 'name', 'description', 'award_type', 'cuisine_type',
            'required_count', 'start_date', 'end_date', 'created_on'
        ]


class AwardSerializer(serializers.ModelSerializer):
    cuisine_type = serializers.CharField(source='cuisine_type.name', read_only=True)

    class Meta:
        model = Award
        fields = [
            'id', 'name', 'description', 'award_type', 'cuisine_type',
            'required_count', 'start_date', 'end_date', 'created_on', "user"
        ]
