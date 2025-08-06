from django import forms
from .models import *

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['date', "note"]


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["title", "description"]


class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ["exercise", "note"]


class SetExerciseForm(forms.ModelForm):
    class Meta:
        model = SetExercise
        fields = ["weight", "repetition"]