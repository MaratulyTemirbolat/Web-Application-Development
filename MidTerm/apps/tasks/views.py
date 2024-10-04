from typing import Any, Type
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response as DRFResponse
from rest_framework.request import Request as DRFRequest
from rest_framework.status import (
    HTTP_200_OK,
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
from apps.abstracts.decorators import validate_serializer_data
from apps.tasks.serializers import (
    UserBaseModelSerializer,
    LoginUserSerializer,
    CreateUserModelSerializer,
    DetailUserModelSerializer,
)
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
