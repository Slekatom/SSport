from django.urls import path
from .views import TrainingListView, TrainingCreateView

urlpatterns = [
    path('', TrainingListView.as_view(), name='training-list'),
    path('create/', TrainingCreateView.as_view(), name="training-create"),
]