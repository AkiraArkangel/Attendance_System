# Generated by Django 5.2 on 2025-04-12 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_meeting_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
