from django.urls import path

from .views import RestaurantCreateApi, UserRestaurantListApiListApi

urlpatterns = [
    path('restaurant-create/', RestaurantCreateApi.as_view(), name='rest_create'),
    path('restaurant-list/', UserRestaurantListApiListApi.as_view(), name='rest_list'),
]
