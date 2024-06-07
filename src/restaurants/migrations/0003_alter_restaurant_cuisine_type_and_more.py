# Generated by Django 4.2.2 on 2024-06-07 05:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_cuisinetype'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0002_remove_restaurant_name_restaurant_place_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='cuisine_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='categories.cuisinetype'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='has_been',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='place_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to=settings.AUTH_USER_MODEL),
        ),
    ]
