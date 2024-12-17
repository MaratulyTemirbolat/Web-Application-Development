# Python
from typing import Type

from rest_framework.serializers import (
    ModelSerializer,
)

from apps.orders.models import Product
from apps.orders.serializers.categories import ForeignCategoryModelSerializer


class BaseProductModelSerializer(ModelSerializer):
    """Product Base model serializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Product] = Product
        fields: str = "__all__"


class ListProductModelSerializer(BaseProductModelSerializer):
    """Serializer for listing products."""

    category: ForeignCategoryModelSerializer = \
        ForeignCategoryModelSerializer()


class ForeignProductModelSerializer(BaseProductModelSerializer):
    """Product serializer as a foreign key."""

    ...
