from django.contrib import admin
from .models import Training

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('date', 'push_up', 'squat', 'press', 'pull_up', 'time_holding')
    list_filter = ('date',)
    search_fields = ('date',)