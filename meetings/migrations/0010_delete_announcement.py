# Generated by Django 5.2 on 2025-05-21 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0009_meeting_google_event_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Announcement',
        ),
    ]
