from django.db import models
from datetime import date
from accounts.models import CustomUser

User = CustomUser

class Training(models.Model):
    date = models.DateField(default=date.today)
    started = models.TimeField(auto_now_add = True)
    ended = models.TimeField(null=True, blank=True)
    note = models.TextField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trainings")

    def __str__(self):
        return f"{self.user}`s training started on {self.date} at {self.started}"

    class Meta:
        verbose_name = "Training"
        verbose_name_plural = "Trainings"


# class ExerciseTitle(models.Model):
#     title = models.CharField(max_length=50, default="")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercisetitles")
#
#     def __str__(self):
#         return f"{self.title}"
#
#     class Meta:
#         verbose_name = "ExerciseTitle"
#         verbose_name_plural = "ExerciseTitles"

class Exercise(models.Model):
    title = models.CharField(max_length=50, default="")
    description = models.TextField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exercises")
    #training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="exercises")
    def __str__(self):
        return f"{self.title} by {self.user}"

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"

class Set(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="sets")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="sets")
    note = models.TextField(max_length=200, blank=True, null=True)
    started = models.TimeField(auto_now=True)
    ended = models.TimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sets")
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Set of {self.exercise} started {self.started}"

    class Meta:
        verbose_name = "Set"
        verbose_name_plural = "Sets"


class SetExercise(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name="setexercises")
    weight = models.PositiveIntegerField(null=True, blank=True)
    repetition = models.PositiveIntegerField(default=15)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="setexercisetrainings")

    def __str__(self):
        return f"{self.set} - {self.weight} - {self.repetition}"

    class Meta:
        verbose_name = "SetExercise"
        verbose_name_plural = "SetExercises"
