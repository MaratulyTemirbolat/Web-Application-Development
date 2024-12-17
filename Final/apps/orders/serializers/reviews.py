# Python
from typing import Type

from rest_framework.serializers import (
    ModelSerializer,
    HiddenField,
    CurrentUserDefault,
)

from apps.orders.models import Review
from apps.auths.serializers import DetailUserModelSerializer


class BaseReviewModelSerializer(ModelSerializer):
    """Review Base model serializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Review] = Review
        fields: str = "__all__"


class CreateReviewModelSerializer(BaseReviewModelSerializer):
    """Serializer to create a new review."""

    user: HiddenField = HiddenField(default=CurrentUserDefault())


class ListReviewModelSerializer(BaseReviewModelSerializer):
    """List all reviews Serializer."""

    user: DetailUserModelSerializer = DetailUserModelSerializer()
