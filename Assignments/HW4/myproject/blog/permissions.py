from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRFRequest

from blog.models import Post


class IsUserAuthor(BasePermission):
    """Class for checking if the user is an author of the post."""
 
    message: str = "Permissions Denied. You are not the author of the post."

    def has_object_permission(self, request: DRFRequest, view: Any, obj: Post):
        return bool(request.user.is_authenticated and obj.author_id == request.user.id)
