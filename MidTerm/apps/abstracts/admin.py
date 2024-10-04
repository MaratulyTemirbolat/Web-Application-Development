from django.contrib.admin import ModelAdmin, register

from apps.tasks.models import Task


@register(Task)
class TaskAdmin(ModelAdmin):
    """Admin class for Task model."""
    ...
