from rest_framework import generics
from .serializers import AwardTypeSerializer
from .models import AwardType


class AwardTypeListApi(generics.ListAPIView):
    serializer_class = AwardTypeSerializer
    queryset = AwardType.objects.all()


class AwardTypeCreateApi(generics.CreateAPIView):
    serializer_class = AwardTypeSerializer
    queryset = AwardType.objects.all()
