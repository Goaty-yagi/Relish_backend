from django.db import models


class AwardType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CuisineType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
