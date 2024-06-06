from rest_framework import generics

from .models import AwardType
from .serializers import AwardTypeSerializer


class AwardTypeListApi(generics.ListAPIView):
    serializer_class = AwardTypeSerializer
    queryset = AwardType.objects.all()


class AwardTypeCreateApi(generics.CreateAPIView):
    serializer_class = AwardTypeSerializer
    queryset = AwardType.objects.all()
