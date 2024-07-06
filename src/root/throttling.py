# users/throttling.py
from typing import Optional

from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.throttling import UserRateThrottle

from users.authentication import CustomJWTAuthentication


class CustomUserRateThrottle(UserRateThrottle):
    def get_ident(self, request: Request) -> str:
        try:
            result: Optional[tuple[AbstractBaseUser, None]
                             ] = CustomJWTAuthentication().authenticate(request)
            if result is not None:
                user, _ = result
                if user:
                    return str(user.UID)
        except AuthenticationFailed:
            pass
        return super().get_ident(request)
