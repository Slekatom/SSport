from django.urls import path
from .views import TrainingListView, TrainingCreateView, training_chart_view

app_name = "main"

urlpatterns = [
    path('', TrainingListView.as_view(), name='training-list'),
    path('create/', TrainingCreateView.as_view(), name="training-create"),
    path('chart/', training_chart_view, name="training-chart"),  # Доданий маршрут для графіка
]
