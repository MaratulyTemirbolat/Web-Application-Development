from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRFRequest

from apps.tasks.models import Task


class IsTaskOwner(BasePermission):
    message: str = "You are not the owner of the task."

    def has_object_permission(
        self, request: DRFRequest, view: Any, obj: Task
    ) -> bool:
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.id == obj.owner_id 
        )