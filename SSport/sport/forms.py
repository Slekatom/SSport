from django import forms
from .models import Training

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['date', 'push_up', 'squat', 'press', 'pull_up', 'time_holding']
