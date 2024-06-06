from typing import Optional

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Location
from .serializers import LocationSerializer


class LocationCreateOrUpdateApi(APIView):
    def post(self, request: Request) -> Response:
        obj, created = Location.objects.get_or_create(**request.data)
        if created:
            obj.save()
        serializer = LocationSerializer(obj)
        return Response(serializer.data)
