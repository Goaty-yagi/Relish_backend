# Generated by Django 4.2.2 on 2024-06-06 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='name',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='place_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
