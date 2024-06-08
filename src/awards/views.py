from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Award, BaseAward
from .serializers import AwardSerializer, BaseAwardSerializer


class AwardListApi(APIView):
    def post(self, request: Request) -> Response:
        try:
            user = request.user
            user_awards = Award.objects.filter(user=user)
            base_award_ids = user_awards.values_list('base_award_id', flat=True)
            base_award_list = BaseAward.objects.exclude(id__in=base_award_ids)
            base_award_serializer = BaseAwardSerializer(base_award_list, many=True)
            award_serializer = AwardSerializer(user_awards, many=True)
            return Response(base_award_serializer.data + award_serializer.data)
        except BaseException:
            return Response("Something wrong happened!", 500)
