from typing import (
    Type,
    Any,
    Optional,
)

from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField,
    ValidationError,
    HiddenField,
    CurrentUserDefault,
)
from rest_framework.exceptions import NotFound

from django.contrib.auth.models import User

from apps.tasks.models import Task


class UserBaseModelSerializer(ModelSerializer):
    """Base model serializer for User model."""

    class Meta:
        model: Type[User] = User
        fields: str = "__all__"
        read_only_fields = [
            'id',
            'date_joined',
            'is_staff',
            'is_active',
        ]


class LoginUserSerializer(Serializer):
    """Serializer class for login user."""

    email: EmailField = EmailField()
    password: CharField = CharField()

    class Meta:
        """Customization of serializer class."""

        fields: tuple[str, str] = (
            "email",
            "password",
        )

    def validate(self, attrs: dict[Any, Any]) -> Any:
        """Validate the email and password."""

        # Extract email and password from the attrs
        email: str = attrs.get("email").lower()
        password: str = attrs.get("password")

        user: Optional[User] = User.objects.filter(email=email).first() 

        # Check if the user exists
        if not user:
            raise NotFound(
                {
                    "email": [
                        f"User with email {email} hasn't been found."
                    ]
                }
            )

        if not user.check_password(raw_password=password):
            raise ValidationError(
                {"password": "The password is incorrect."}
            )

        # Check if the user's account is active
        if not user.is_active:
            raise ValidationError(
                {"email": "Your account is not active."}
            )

        # If email exists and password is correct, add the user object to validated_data
        attrs['user'] = user
        return super().validate(attrs)


class DetailUserModelSerializer(ModelSerializer):
    """Model serializer for User model."""

    class Meta:
        model: Type[User] = User
        exclude: tuple[str, ...] = (
            'password',
            'groups',
            'user_permissions',
            "username",
        )
        read_only_fields = [
            'id',
            'date_joined',
            'is_staff',
            'is_active',
        ]


class CreateUserModelSerializer(ModelSerializer):
    """Serializer class to create a user."""

    email: EmailField = EmailField()
    username: CharField = CharField(
        required=False,
    )
    first_name: CharField = CharField()

    class Meta:
        """Customization of serializer class."""

        model: Type[User] = User
        fields: tuple[str, str, str] = (
            "username",
            'email',
            'password',
            'first_name',
            "last_name",
        )
        extra_kwargs: dict[str, Any] = {
            'password': {'write_only': True},
        }

    def validate_email(self, value: str) -> str:
        """Ensure the email is unique."""
        email: str = value.lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists.")
        return email

    def to_internal_value(self, data: dict[str, Any]) -> dict[str, Any]:
        value: dict[str, Any] = super().to_internal_value(data)
        value["email"] = value["email"].lower()
        value["is_staff"] = False
        value["is_superuser"] = False
        value["is_active"] = True
        value["username"] = value["email"].lower()
        return value


class TaskBaseModelSerializer(ModelSerializer):
    """Base serializer for Task model."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Task] = Task
        fields: str = "__all__"

    def to_representation(self, instance: Task) -> dict[str, Any]:
        representation: dict[str, Any] = super().to_representation(instance)
        representation["status"] = Task.get_status_dict(
            status_id=representation["status"]
        )
        return representation


class TaskListModelSerializer(TaskBaseModelSerializer):
    """Serializer to list the Tasks."""

    ...


class TaskCreateModelSerializer(TaskBaseModelSerializer):
    """Serializer to create a noew Task."""

    owner: HiddenField = HiddenField(default=CurrentUserDefault())

    class Meta:
        """Customization of the Serializer."""

        model: Type[Task] = Task
        exclude: tuple[str] = (
            "status",
        )


class TaskDetailModelSerializer(TaskBaseModelSerializer):
    """Serializer to view detailed information about the task."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Task] = Task
        fields: str = "__all__"


class TaskPartialUpdateModelSerializer(TaskBaseModelSerializer):
    """Serializer to partially update task's data."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Task] = Task
        fields: tuple[str] = (
            "status",
        )

    def validate_status(self, value: int) -> int:
        """Validate that the status is valid."""
        if value not in Task.get_status_dict(status_id=value):
            raise ValidationError("Invalid status.")
        elif value == self.instance.status:
            raise ValidationError("You can't update the task with the same status.")
        return value

