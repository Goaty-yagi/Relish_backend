from django.urls import path

from .views import AwardListApi

urlpatterns = [
    path('award-list/', AwardListApi.as_view(), name='rest_create'),
]
