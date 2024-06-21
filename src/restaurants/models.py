from django.db import models
from django.utils import timezone

from categories.models import CuisineType
from users.models import User


class Restaurant(models.Model):
    place_id = models.CharField(max_length=100, blank=False)
    obj = models.CharField(max_length=30000)
    cuisine_type = models.ForeignKey(
        CuisineType,
        related_name='restaurant',
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE
    )
    has_been = models.BooleanField()
    is_favorite = models.BooleanField(default=False)
    user_id = models.ForeignKey(
        User,
        related_name='restaurant',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['-created_on',]
