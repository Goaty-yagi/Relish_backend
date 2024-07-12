from typing import Any

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

from categories.models import AwardType, CuisineType
from restaurants.models import Restaurant
from users.models import User


class BaseAward(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    description = models.CharField(max_length=120, blank=True)
    award_type = models.ForeignKey(
        AwardType,
        related_name='base_awards',
        null=False,
        on_delete=models.CASCADE
    )
    cuisine_type = models.ForeignKey(
        CuisineType,
        related_name='base_awards',
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE
    )
    required_count = models.PositiveIntegerField(default=1)
    start_date = models.DateTimeField(default=None, blank=True, null=True)
    end_date = models.DateTimeField(default=None, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['-created_on',]

    def __str__(self) -> str:
        return f"A: {self.award_type.name} C: {self.cuisine_type} : {self.required_count}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.award_type.name == 'cuisine':
            self.description = f"Visited {self.required_count} new {self.cuisine_type.name} " \
                f"{'restaurant' if self.required_count == 1 else 'restaurants'}"
        elif self.award_type.name == 'sum':
            if self.cuisine_type:
                raise ValidationError("If Award type is sum, cuisine type should be Null.")
            self.description = f"Visited {self.required_count} new "\
                f"{'restaurant' if self.required_count == 1 else 'restaurants'}"

        if not self.description:
            raise ValidationError("Description cannot be generated as award_type is missing.")
        super().save(*args, **kwargs)


class Award(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=120)
    award_type = models.ForeignKey(
        AwardType,
        related_name='awards',
        null=False,
        on_delete=models.CASCADE
    )
    cuisine_type = models.ForeignKey(
        CuisineType,
        related_name='awards',
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE
    )
    base_award = models.ForeignKey(
        BaseAward,
        related_name='awards',
        null=False,
        on_delete=models.PROTECT
    )
    required_count = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(
        User,
        related_name='awards',
        on_delete=models.CASCADE
    )
    start_date = models.DateTimeField(default=None, blank=True, null=True)
    end_date = models.DateTimeField(default=None, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['-created_on',]

    def __str__(self) -> str:
        return self.name


@receiver(post_save, sender=Restaurant)
def handle_restaurant_creation(
        sender: Restaurant, instance: Restaurant, created: bool, **kwargs: Any) -> None:
    if created:
        user: str = instance.user_id
        cuisine_type = instance.cuisine_type
        restaurant_sum: int = Restaurant.objects.filter(user_id=user).count()

        # Handle sum type award
        min_required_obj = BaseAward.objects.filter(
            award_type__name='sum',
            required_count__gte=restaurant_sum
        ).order_by('required_count').first()
        if min_required_obj:
            if min_required_obj.required_count <= restaurant_sum:
                if not Award.objects.filter(base_award=min_required_obj).exists():
                    obj = {
                        'name': min_required_obj.name,
                        'description': min_required_obj.description,
                        'award_type': min_required_obj.award_type,
                        'required_count': min_required_obj.required_count,
                    }
                    Award.objects.create(user=user, base_award=min_required_obj, **obj)
                    print("Created sum award")

        # Handle cuisine type awards
        cuisine_type_restaurant_sum = Restaurant.objects.filter(
            user_id=user, cuisine_type=cuisine_type).count()
        min_required_obj = BaseAward.objects.filter(
            award_type__name='cuisine',
            cuisine_type=cuisine_type,
            required_count__gte=cuisine_type_restaurant_sum
        ).order_by('required_count').first()
        if min_required_obj:
            if min_required_obj.required_count == cuisine_type_restaurant_sum:
                if not Award.objects.filter(base_award=min_required_obj).exists():
                    obj = {
                        'name': min_required_obj.name,
                        'description': min_required_obj.description,
                        'award_type': min_required_obj.award_type,
                        'cuisine_type': min_required_obj.cuisine_type,
                        'required_count': min_required_obj.required_count,
                    }
                    Award.objects.create(user=user, base_award=min_required_obj, **obj)
                    print("Created cuisine award")


@receiver(pre_delete, sender=Restaurant)
def handle_restaurant_deletion(
        sender: Restaurant, instance: Restaurant, **kwargs: Any) -> None:
    user: str = instance.user_id
    cuisine_type = instance.cuisine_type
    restaurant_sum: int = Restaurant.objects.filter(user_id=user).count() - 1

    # Handle sum type award
    max_required_award = Award.objects.filter(
        award_type__name='sum',
        required_count__gt=restaurant_sum
    ).order_by('required_count').first()
    if max_required_award:
        if max_required_award.required_count > restaurant_sum:
            max_required_award.delete()
            print("DELETED SumAward")

    # Handle cuisine type awards
    cuisine_type_restaurant_sum = Restaurant.objects.filter(
        user_id=user, cuisine_type=cuisine_type).count() - 1
    max_required_award = Award.objects.filter(
        award_type__name='cuisine',
        cuisine_type=cuisine_type,
        required_count__gt=cuisine_type_restaurant_sum
    ).order_by('required_count').first()
    if max_required_award:
        if max_required_award.required_count > cuisine_type_restaurant_sum:
            max_required_award.delete()
            print("DELETED CuisineAward")
