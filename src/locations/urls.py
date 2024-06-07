from django.urls import path

from .views import LocationListApi

urlpatterns = [
    path('location-list/', LocationListApi.as_view()),
]
