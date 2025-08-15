import io
import base64
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Виправлення помилки Matplotlib у Django
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *


# Мапінг назв з GET-запиту на поля у БД
# EXERCISE_MAPPING = {
#     "push_ups": "push_up",
#     "squats": "squat",
#     "presses": "press",
#     "pull_ups": "pull_up",
#     "time_holding": "time_holding",
# }
#
# def training_chart_view(request, user):
#     form = ChartForm(request.GET or None)
#     exercise = Exercise.objects.filter(user = request.user).first()
#     exercise_type = ""
#     start_date = request.GET.get("start_date", "2025-08-01")
#     end_date = request.GET.get("end_date", "2025-08-15")
#     if form.is_valid():
#         exercise_type = form.cleaned_data.get("title", "") # Значення за замовчуванням
#
#     # Конвертація у формат `datetime`
#     start_date = parse_date(start_date)
#     end_date = parse_date(end_date)
#     print(start_date)
#     print(end_date)
#     print(exercise_type)
#
#     # Отримуємо правильне поле з БД
#     exercise_field = EXERCISE_MAPPING.get(exercise_type, exercise)
#
#     # Фільтрація тренувань за датою
#     trainings = Training.objects.filter(started__range=(start_date, end_date)).order_by("started")
#
#     # Формуємо дані для графіка
#     if trainings.exists():
#         data = [{"date": t.date, "value": getattr(t, exercise_field, 0)} for t in trainings]
#     else:
#         data = [{"date": start_date, "value": 0}, {"date": end_date, "value": 0}]
#
#     df = pd.DataFrame(data)
#     df["date"] = pd.to_datetime(df["date"])
#
#     # Побудова графіка
#     plt.figure(figsize=(8, 4))
#     plt.plot(df["date"], df["value"], marker="o", linestyle="-", color="blue", label="Training Progress")
#     plt.xlabel("Дата")
#     plt.ylabel("Кількість повторень")
#     plt.title(f"Прогрес тренувань")
#     plt.legend()
#     plt.grid()
#
#     # Збереження графіка в пам'ять
#     buf = io.BytesIO()
#     plt.savefig(buf, format="png")
#     buf.seek(0)
#     string = base64.b64encode(buf.read()).decode("utf-8")
#     uri = "data:image/png;base64," + string
#     buf.close()
#
#     return render(request, "sport/training_chart.html", {
#         "chart": uri,
#         "start_date": start_date,
#         "end_date": end_date,
#         "exercise_type": exercise_type,
#         "form": form,
#     })

class ChartView(FormView):
    template_name = "sport/training_chart.html"
    form_class = ChartForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercise_id = self.request.GET.get("exercise")
        start_date_raw = self.request.GET.get("start_date")
        end_date_raw = self.request.GET.get("end_date")

        if exercise_id and start_date_raw and end_date_raw:
            start_date = parse_date(start_date_raw)
            end_date = parse_date(end_date_raw)
            exercise = Exercise.objects.get(id=exercise_id)

            exercises_qs = SetExercise.objects.filter(
                training__user=self.request.user,
                exercise=exercise,
                started__range=(start_date, end_date)
            )

            if exercises_qs.exists():
                print(exercises_qs)
            else:
                print("None")

            context["exercises_qs"] = exercises_qs

        return context




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
        context["exercises"] = SetExercise.objects.filter(training = self.get_object())
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
        set_id = self.object.id
        return reverse_lazy("main:set_exercise-create", kwargs={"training_id": training_id, "set_id": set_id})


class SetExerciseCreateView(CreateView):
    model = SetExercise
    template_name = "sport/set_exercise.html"
    form_class = SetExerciseForm

    def form_valid(self, form):
        set_id = self.kwargs.get("set_id")
        set = Set.objects.get(id = set_id, user = self.request.user)
        form.instance.set = set
        form.instance.training = set.training
        form.instance.started = set.started
        form.instance.ended = set.ended
        form.instance.exercise = set.exercise
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_id = self.kwargs.get("set_id")
        set = Set.objects.get(id=set_id, user=self.request.user)
        context["set"] = set
        return context

    def get_success_url(self):
        training_id = self.object.set.training.id
        return reverse_lazy("main:detail", kwargs={"pk": training_id})





