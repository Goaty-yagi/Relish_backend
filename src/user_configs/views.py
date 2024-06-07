from typing import Optional

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from locations.models import Location

from .models import UserConfig
from .serializers import UserConfigSerializer


class UserConfigCreateApi(APIView):
    def post(self, request: Request) -> Response:
        user = request.user
        user_config: Optional[UserConfig] = UserConfig.objects.filter(user_id=user).first()

        if user_config:
            location = user_config.location
            for attr, value in request.data.items():
                setattr(location, attr, value)
            location.save()
        else:
            location_data = request.data
            location = Location.objects.create(**location_data)
            user_config = UserConfig.objects.create(user_id=user, location=location)

        serializer = UserConfigSerializer(user_config)

        status_code = 201 if not user_config else 200
        return Response(serializer.data, status=status_code)
