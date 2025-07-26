from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    description = models.TextField(max_length=100)
    birthdate = models.PositiveIntegerField(null=True, blank = True)
    password = models.CharField(max_length=120)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.username