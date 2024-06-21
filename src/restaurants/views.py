from typing import Optional

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.models import CuisineType

from .models import Restaurant
from .serializers import RestaurantCreateSerializer


class RestaurantCreateApi(APIView):
    def post(self, request: Request) -> Response:
        place_id: Optional[str] = request.data.get('place_id')
        user = request.user
        existing_restaurant = Restaurant.objects.filter(place_id=place_id, user_id=user)
        if existing_restaurant.exists():
            existing_restaurant.delete()
            return Response({'message': 'Successfully deleted!'}, 204)
        cuisine_type: Optional[str] = request.data.pop('cuisine_type').lower()
        if cuisine_type:
            request.data['cuisine_type'] = CuisineType.objects.get_or_create(name=cuisine_type)[0]

        user = request.user

        restaurant = Restaurant.objects.create(user_id=user, **request.data)
        serializer = RestaurantCreateSerializer(restaurant)
        return Response(serializer.data)


class UserRestaurantListApiListApi(APIView):
    def post(self, request: Request) -> Response:
        user = request.user
        restaurant_list = Restaurant.objects.filter(user_id=user)
        serializer = RestaurantCreateSerializer(restaurant_list, many=True)
        return Response(serializer.data)
