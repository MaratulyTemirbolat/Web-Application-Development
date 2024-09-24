from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    IntegerField,
    CASCADE,
)
from django.contrib.auth.models import User

from apps.abstracts.models import AbstractBaseModel


class Task(AbstractBaseModel):
    """Class to represent a task database model."""

    TITLE_MAX_LENGTH: int = 150
    STATUS_DONE = 1
    STATUS_DONE_TEXT = 'Done'
    STATUS_IN_PROGRESS = 2
    STATUS_IN_PROGRESS_TEXT = 'In progress'
    STATUS_PLANNED = 3
    STATUS_PLANNED_TEXT = 'Planned'
    STATUS_CANCELLED = 4
    STATUS_CANCELLED_TEXT = 'Cancelled'
    STATUS_CHOICES = (
        (STATUS_DONE, STATUS_DONE_TEXT),
        (STATUS_IN_PROGRESS, STATUS_IN_PROGRESS_TEXT),
        (STATUS_PLANNED, STATUS_PLANNED_TEXT),
        (STATUS_CANCELLED, STATUS_CANCELLED_TEXT),
    )

    # Title of the task.
    title: str = CharField(
        max_length=TITLE_MAX_LENGTH,
        db_index=True,
        verbose_name='Title',
        help_text="Title of the task."
    )
    # Description of the task.
    description: str = TextField(
        blank=True,
        null=True,
        verbose_name='Description',
        help_text="Description of the task (detailed explanation)."
    )
    # Owner of the task.
    owner: User = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="tasks",
        verbose_name='Owner',
        help_text="Owner of the task."
    )
    # Status of the task.
    status: int = IntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_PLANNED,
        verbose_name="Status",
        help_text="Status of the task."
    )

    class Meta:
        """Meta class for Task model."""

        verbose_name: str = 'Task'
        verbose_name_plural: str = 'Tasks'
