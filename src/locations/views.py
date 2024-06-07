from rest_framework import generics

from .models import Location
from .serializers import LocationSerializer


class LocationListApi(generics.ListAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
