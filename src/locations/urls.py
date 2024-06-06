from django.urls import path
from .views import LocationCreateOrUpdateApi

urlpatterns = [
    path('location-create-update/', LocationCreateOrUpdateApi.as_view()),
]
