import io
import base64
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Виправлення помилки Matplotlib у Django
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.views.generic import ListView, CreateView
from django.urls import reverse
from .models import Training
from .forms import TrainingForm

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
    template_name = "training.html"
    context_object_name = "trainings"
    ordering = ['-date']

# Створення нового тренування
class TrainingCreateView(CreateView):
    model = Training
    template_name = "training_create.html"
    form_class = TrainingForm

    def get_success_url(self):
        return reverse("training-list")
