from django.db import models


class Location(models.Model):
    latitude = models.IntegerField()
    longitude = models.IntegerField()

    def __str__(self) -> str:
        return self.id
