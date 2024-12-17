# Python
from typing import Type

from rest_framework.serializers import (
    ModelSerializer,
)

from apps.orders.models import Category


class BaseCategoryModelSerializer(ModelSerializer):
    """Category Base model serializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Category] = Category
        fields: str = "__all__"


class ForeignCategoryModelSerializer(BaseCategoryModelSerializer):
    """Foreign cases where Categorory is used."""

    ...
