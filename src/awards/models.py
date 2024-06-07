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
    user_id = models.ForeignKey(
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
    print("CREATED:", instance.__dict__, sender)
    if created:
        user = instance.user_id
        cuisine_type = instance.cuisine_type
        restaurant_sum = Restaurant.objects.filter(user_id=user).count()
        print("restaurant_list", restaurant_sum)

        # min_required_count = BaseAward.objects.filter(
        #     award_type__name='sum',
        #     required_count__gt=restaurant_sum
        # ).aggregate(min_required_count=Min('required_count'))['min_required_count']
        min_required_obj = BaseAward.objects.filter(
            award_type__name='sum',
            required_count__gte=restaurant_sum
        ).order_by('required_count').first()
        # Might need to migrate 
        # if min_required_count == restaurant_sum:
        #     if Award.objects.filter(base_award=)
        print("min_required_count", min_required_obj.__dict__)
        # Logic to handle creation
        print("Restaurant created:", instance)


@receiver(pre_delete, sender=Restaurant)
def handle_restaurant_deletion(sender, instance, **kwargs):
    # Logic to handle deletion
    user = instance.user_id
    restaurant_sum = Restaurant.objects.filter(user_id=user).count()
    print("Restaurant deleted:", instance.user_id)

# @receiver(post_save, sender=Restaurant)
# def award_handling_by_restaurant_changes(sender, instance, created, **kwargs):
#     if created:
#         print("RECeiVER")
#         ids = ["ボキャブラリー","ひらがな","カタカナ","すうじ"]
#         MyQuiz.objects.create(user=instance)
#         grade = ParentQuiz.objects.get(name="超初級")
#         quiz_taker = QuizTaker.objects.create(user=instance, grade=grade)
#         status = ParentStatus.objects.filter(name__in=ids)
#         for i in status:
#             UserStatus.objects.create(quiz_taker=quiz_taker, status=i, grade=grade)
#         return quiz_taker
