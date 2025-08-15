from django.urls import path
from .views import TrainingListView, TrainingCreateView, ChartView, TrainingDetailView, ExerciseCreateView, SetCreateView, SetExerciseCreateView

app_name = "main"

urlpatterns = [
    path('', TrainingListView.as_view(), name='training-list'),
    path('training/<int:pk>/', TrainingDetailView.as_view(), name="detail"),
    path('training/create/', TrainingCreateView.as_view(), name="training-create"),
    path('<str:user>/chart/', ChartView.as_view(), name="training-chart"),  # Доданий маршрут для графіка
    path('exercise/<int:tr_pk>/create/', ExerciseCreateView.as_view(), name = "exercise"),
    path("training/<int:training_id>/set/create/", SetCreateView.as_view(), name="set-create"),
    path("training/<int:training_id>/set/<int:set_id>/create/", SetExerciseCreateView.as_view(), name="set_exercise-create"),
]
