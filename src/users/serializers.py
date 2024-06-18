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

class UserTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

