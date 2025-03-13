from django.urls import path
from .views import TrainingListView

urlpatterns = [
    path('', TrainingListView.as_view(), name='training-list'),
]
