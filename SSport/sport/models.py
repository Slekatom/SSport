from django.db import models
from datetime import date

class Training(models.Model):
    date = models.DateField(default=date.today)
    push_up = models.PositiveIntegerField(default=0)
    squat = models.PositiveIntegerField(default=0)
    press = models.PositiveIntegerField(default=0)
    pull_up = models.PositiveIntegerField(default=0)
    time_holding = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Training"
        verbose_name_plural = "Trainings"
    
    def __str__(self):
        return f"""Training at {self.date}. You made {self.push_up} push-ups,
        {self.squat} squat, {self.press} press, {self.pull_up} pull-ups,
        holding time is {self.time_holding}"""