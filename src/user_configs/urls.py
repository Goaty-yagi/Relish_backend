from django.urls import path

from .views import UserConfigCreateApi

urlpatterns = [
    path('user-config-crate-update/', UserConfigCreateApi.as_view(), name='u-config-create'),
]
