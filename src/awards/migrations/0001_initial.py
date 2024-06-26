# Generated by Django 4.2.2 on 2024-06-07 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0002_cuisinetype'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseAward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=120)),
                ('required_count', models.IntegerField(default=0)),
                ('start_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('end_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('created_on', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('award_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_awards', to='categories.awardtype')),
                ('cuisine_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_awards', to='categories.cuisinetype')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=120)),
                ('required_count', models.IntegerField(default=0)),
                ('start_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('end_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('created_on', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('award_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awards', to='categories.awardtype')),
                ('cuisine_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='awards', to='categories.cuisinetype')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
