from typing import Optional
from uuid import uuid4

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, password: Optional[str] = None) -> 'User':
        if not email:
            raise ValueError('email is required')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username: str, email: str, password: str) -> 'User':
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    UID = models.CharField(max_length=255, default=uuid4,
                           primary_key=True, unique=True, editable=False)
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    avatar = models.CharField(max_length=100, default=None, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-created_on',]

    def __str__(self) -> str:
        return self.username
