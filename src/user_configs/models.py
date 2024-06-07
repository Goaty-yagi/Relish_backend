from django.db import models

from locations.models import Location
from users.models import User


class UserConfig(models.Model):
    location = models.OneToOneField(
        Location,
        on_delete=models.CASCADE
    )
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'UserConfig(id={self.id}'
