from django.db import models
from datetime import date

class Training(models.Model):
    date = models.DateField(default=date.today)
    # push_up = models.PositiveIntegerField(default=0)
    # squat = models.PositiveIntegerField(default=0)
    # #press = models.PositiveIntegerField(default=0)
    # pull_up = models.PositiveIntegerField(default=0)
    # time_holding = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Training"
        verbose_name_plural = "Trainings"
    
class Exercise(models.Model):
    title = models.CharField(max_length=50, default="")
