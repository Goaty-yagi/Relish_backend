from django.urls import path
from .views import AwardTypeListApi, AwardTypeCreateApi

urlpatterns = [
    path('award-type-list/', AwardTypeListApi.as_view()),
    path('award-type-create/', AwardTypeCreateApi.as_view()),
]
