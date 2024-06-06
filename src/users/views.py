from typing import Any, Dict, Tuple

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,
                                            TokenVerifyView)


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        # rest of the method...


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        # rest of the method...


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        # rest of the method...


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        # rest of the method...


class LogoutView(APIView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = Response(status=status.HTTP_204_NO_CONTENT)
        # rest of the method...
