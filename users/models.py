from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=30)
    position = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=15, unique=True)
    
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    ]
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)

    def __str__(self):
        return self.user.get_full_name()
