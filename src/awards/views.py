from typing import Optional

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import BaseAward, Award
from .serializers import BaseAwardSerializer


class AwardListApi(APIView):
    def post(self, request: Request) -> Response:
        user = request.user
        base_award_list = BaseAward.objects.all()
        serializer = BaseAwardSerializer(base_award_list, many=True)
        return Response(serializer.data)

