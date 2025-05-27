from django.db import models
from django.contrib.auth.models import User

class Meeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    ended = models.BooleanField(default=False)
    google_event_id = models.CharField(max_length=256, blank=True, null=True)
    agenda = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} on {self.date}"

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'meeting')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.meeting.title}"
