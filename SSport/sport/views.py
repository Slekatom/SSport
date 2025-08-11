import io
import base64
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Виправлення помилки Matplotlib у Django
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *
# Мапінг назв з GET-запиту на поля у БД
EXERCISE_MAPPING = {
    "push_ups": "push_up",
    "squats": "squat",
    "presses": "press",
    "pull_ups": "pull_up",
    "time_holding": "time_holding",
}

def training_chart_view(request):
    start_date = request.GET.get("start_date", "2024-03-01")
    end_date = request.GET.get("end_date", "2024-03-05")
    exercise_type = request.GET.get("exercise_type", "squats")  # Значення за замовчуванням

    # Конвертація у формат `datetime`
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    # Отримуємо правильне поле з БД
    exercise_field = EXERCISE_MAPPING.get(exercise_type, "squat")

    # Фільтрація тренувань за датою
    trainings = Training.objects.filter(date__range=(start_date, end_date)).order_by("date")

    # Формуємо дані для графіка
    if trainings.exists():
        data = [{"date": t.date, "value": getattr(t, exercise_field, 0)} for t in trainings]
    else:
        data = [{"date": start_date, "value": 0}, {"date": end_date, "value": 0}]

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    # Побудова графіка
    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["value"], marker="o", linestyle="-", color="blue", label="Training Progress")
    plt.xlabel("Дата")
    plt.ylabel("Кількість повторень")
    plt.title(f"Прогрес тренувань: {exercise_field.replace('_', ' ').capitalize()}")
    plt.legend()
    plt.grid()

    # Збереження графіка в пам'ять
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode("utf-8")
    uri = "data:image/png;base64," + string
    buf.close()

    return render(request, "training_chart.html", {
        "chart": uri,
        "start_date": start_date,
        "end_date": end_date,
        "exercise_type": exercise_type,
    })

# Список тренувань
class TrainingListView(ListView):
    model = Training
    template_name = "sport/training.html"
    context_object_name = "trainings"
    ordering = ['date']

# Створення нового тренування
class TrainingCreateView(CreateView):
    model = Training
    template_name = "sport/training_create.html"
    form_class = TrainingForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("main:training-list")

class TrainingDetailView(DetailView):
    model = Training
    template_name = "sport/training_detail.html"
    context_object_name = "training"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        training = self.get_object()
        context["sets"] = training.sets.all()
        context["set"] = training.sets.first()
        return context

class ExerciseCreateView(CreateView):
    model = Exercise
    template_name = "sport/exercise.html"
    form_class = ExerciseForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        training_id = self.kwargs.get("tr_pk")
        return reverse_lazy("main:detail", kwargs={"pk": training_id})

class SetCreateView(CreateView):
    model = Set
    template_name = "sport/set.html"
    form_class = SetForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        training_id = self.kwargs.get("training_id")
        training = Training.objects.get(id=training_id, user=self.request.user)
        form.instance.training = training
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        training_id = self.kwargs.get("training_id")
        return reverse_lazy("main:detail", kwargs={"pk": training_id})

class SetExerciseCreateView(CreateView):
    model = SetExercise
    template_name = "sport/set_exercise.html"
    form_class = SetExerciseForm

    def form_valid(self, form):
        set_id = self.kwargs.get("set_id")
        set = Set.objects.get(id = set_id, user = self.request.user)
        form.instance.set = set
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("main:training-list")



