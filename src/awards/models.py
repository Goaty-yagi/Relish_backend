from django.db import models
from django.utils import timezone

from categories.models import CuisineType
from users.models import User
from categories.models import AwardType, CuisineType
from restaurants.models import Restaurant

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Min


class BaseAward(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=120)
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
    required_count = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=None, blank=True, null=True)
    end_date = models.DateTimeField(default=None, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['-created_on',]

    def __str__(self) -> str:
        return self.name


class Award(models.Model):
    name = models.CharField(max_length=100, unique=True)
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
        on_delete=models.DO_NOTHING
    )
    required_count = models.IntegerField(default=0)
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
def handle_restaurant_creation(sender, instance, created, **kwargs):
    if created:
        user = instance.user_id
        cuisine_type = instance.cuisine_type
        restaurant_sum = Restaurant.objects.filter(user_id=user).count()

        # Handle sum type award
        min_required_obj = BaseAward.objects.filter(
            award_type__name='sum',
            required_count__gte=restaurant_sum
        ).order_by('required_count').first()
        if min_required_obj:
            if min_required_obj.required_count == restaurant_sum:
                if not Award.objects.filter(base_award=min_required_obj).exists():
                    obj = {
                        'name': min_required_obj.name,
                        'description': min_required_obj.description,
                        'award_type': min_required_obj.award_type,
                        'required_count': min_required_obj.required_count,
                    }
                    Award.objects.create(user=user, base_award=min_required_obj, **obj)

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


@receiver(pre_delete, sender=Restaurant)
def handle_restaurant_deletion(sender, instance, **kwargs):
    # Logic to handle deletion
    user = instance.user_id
    restaurant_sum = Restaurant.objects.filter(user_id=user).count()
    print("Restaurant deleted:", instance.user_id)