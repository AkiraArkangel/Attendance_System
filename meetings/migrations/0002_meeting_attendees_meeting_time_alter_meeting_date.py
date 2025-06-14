# Generated by Django 5.2 on 2025-04-06 05:57

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='attendees',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meeting',
            name='time',
            field=models.TimeField(default=datetime.time(12, 0)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(),
        ),
    ]
