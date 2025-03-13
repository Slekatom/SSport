from django.shortcuts import render, reverse
from django.views.generic import ListView, CreateView
from .models import Training
from .forms import TrainingForm

class TrainingListView(ListView):
    model = Training
    template_name = "training.html"
    context_object_name = "trainings"
    ordering = ['-date']

class TrainingCreateView(CreateView):
    model = Training
    template_name = "training_create.html"
    form_class = TrainingForm
    def get_success_url(self):
        return reverse("training-list")
