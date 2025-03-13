from django.shortcuts import render
from .models import Training
from django.views.generic import ListView


class TrainingListView(ListView):
    model = Training
    template_name = "training.html"
    context_object_name = "trainings"

