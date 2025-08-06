from django.urls import path
from .views import TrainingListView, TrainingCreateView, training_chart_view, TrainingDetailView, ExerciseCreateView, SetCreateView, SetExerciseCreateView

app_name = "main"

urlpatterns = [
    path('', TrainingListView.as_view(), name='training-list'),
    path('training/<str:user>/<int:pk>/', TrainingDetailView.as_view(), name="detail"),
    path('training/create/', TrainingCreateView.as_view(), name="training-create"),
    path('<str:user>/chart/', training_chart_view, name="training-chart"),  # Доданий маршрут для графіка
    path('exercise/create/', ExerciseCreateView.as_view(), name = "exercise"),
    path("trainings/<int:training_id>/sets/create/", SetCreateView.as_view(), name="set-create"),
    path("trainings/<int:training_id>/<int:set_id>/create/", SetExerciseCreateView.as_view(), name="set_exercise-create"),
]
