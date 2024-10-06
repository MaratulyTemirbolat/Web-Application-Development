from typing import Any, Type
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response as DRFResponse
from rest_framework.request import Request as DRFRequest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_501_NOT_IMPLEMENTED,
)
from rest_framework.permissions import (
    IsAuthenticated,
    BasePermission,
    AllowAny,
)
from rest_framework.decorators import action

from django.contrib.auth.models import User
from django.db.models import Manager, QuerySet
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password

from apps.abstracts.handlers import DRFResponseHandler
from apps.abstracts.decorators import (
    validate_serializer_data,
    find_queryset_object_by_query_pk,
)
from apps.tasks.serializers import (
    UserBaseModelSerializer,
    LoginUserSerializer,
    CreateUserModelSerializer,
    DetailUserModelSerializer,
    TaskBaseModelSerializer,
    TaskCreateModelSerializer,
    TaskListModelSerializer,
    TaskDetailModelSerializer,
    TaskPartialUpdateModelSerializer,
)
from apps.tasks.models import Task
from apps.tasks.permissions import IsTaskOwner
from utils.helpers import generate_secure_random_string


class UserViewSet(DRFResponseHandler, ViewSet):
    """View set to handler User related requests."""

    queryset: Manager = User.objects
    permission_classes: tuple[Type[BasePermission]] = (IsAuthenticated,)
    serializer_class: Type[UserBaseModelSerializer] = UserBaseModelSerializer

    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Method to handle list request."""
        return DRFResponse(
            status=HTTP_501_NOT_IMPLEMENTED
        )

    @action(
        methods=["POST"],
        detail=False,
        url_path="login",
        url_name="login",
        permission_classes=(AllowAny,),
        authentication_classes=[],
    )
    @validate_serializer_data(
        serializer_class=LoginUserSerializer
    )
    def login(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Method to handle login request."""
        user: User = kwargs.get("validated_data").get("user")
        # login(request=request, user=user)

        # Generate refresh and access tokens for the user and set into response data
        refresh_token: RefreshToken = RefreshToken.for_user(user=user)
        response: DRFResponse = DRFResponse(
            data=DetailUserModelSerializer(
                instance=user,
                many=False
            ).data,
            status=HTTP_200_OK
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh_token),
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.set_cookie(
            key='access_token',
            value=f"JWT {str(refresh_token.access_token)}",
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.set_cookie(
            key="csrftoken",
            value=generate_secure_random_string(length=64),
            httponly=False,
            secure=True,
            samesite='Lax',
        )
        return response

    @action(
        methods=["POST"],
        detail=False,
        url_path="register",
        url_name="register",
        permission_classes=(AllowAny,),
        authentication_classes=[],
    )
    @validate_serializer_data(
        serializer_class=CreateUserModelSerializer
    )
    def register_user(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Method to handle register user request."""
        serializer: CreateUserModelSerializer = kwargs.get("serializer")
        new_user: User = serializer.save()
        new_user.password = make_password(password=request.data["password"])
        new_user.save(update_fields=["password"])
        return DRFResponse(
            data=DetailUserModelSerializer(
                instance=new_user,
                many=False
            ).data,
            status=HTTP_200_OK
        )


class TaskViewSet(DRFResponseHandler, ViewSet):
    """View set to handler Task related requests."""

    queryset: Manager = Task.objects
    permission_classes: tuple[
        Type[BasePermission],
        Type[BasePermission]
    ] = (
        IsAuthenticated,
        IsTaskOwner,
    )
    serializer_class: Type[TaskBaseModelSerializer] = TaskBaseModelSerializer
    authentication_classes: list[Any] = []

    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle GET-request to get all the tasks."""

        return self.get_drf_response(
            request=request,
            data=request.user.tasks.all(),
            serializer_class=TaskListModelSerializer,
            many=True
        )

    @validate_serializer_data(
        serializer_class=TaskCreateModelSerializer
    )
    def create(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handler POST-request to create a new task instance."""

        serializer: TaskCreateModelSerializer = kwargs.get("serializer")
        new_task: Task = serializer.save()
        return self.get_drf_response(
            request=request,
            data=new_task,
            serializer_class=TaskDetailModelSerializer
        )

    @find_queryset_object_by_query_pk(
        queryset=Task.objects,
        class_name=Task,
        entity_name="Task"
    )
    def delete(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...], 
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle DELETE-request to drop your owned task."""
        task: Task = kwargs.get("object")
        self.check_object_permissions(request=request, obj=task)
        task.delete()
        return DRFResponse(
            data="Your task has been succesfully deleted",
            status=HTTP_204_NO_CONTENT
        )

    @find_queryset_object_by_query_pk(
        queryset=Task.objects,
        class_name=Task,
        entity_name="Task"
    )
    @validate_serializer_data(
        serializer_class=TaskPartialUpdateModelSerializer
    )
    def partial_update(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle PATCH-request to change task's status."""
        task: Task = kwargs.get("object")
        serializer: TaskPartialUpdateModelSerializer = TaskPartialUpdateModelSerializer(
            instance=task,
            data=request.data,
            partial=True
        )
        serializer.save()
        return DRFResponse(
            data=TaskDetailModelSerializer(
                instance=task,
                many=False
            ).data,
            status=HTTP_200_OK
        )
