from django.urls import path

from .views import AwardTypeCreateApi, AwardTypeListApi

urlpatterns = [
    path('award-type-list/', AwardTypeListApi.as_view()),
    path('award-type-create/', AwardTypeCreateApi.as_view()),
]
