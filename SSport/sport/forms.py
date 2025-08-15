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

class ChartForm(forms.ModelForm):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Charts
        fields = ["exercise", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={'type': 'date'}),
            "end_date": forms.DateInput(attrs={'type': 'date'}),
        }