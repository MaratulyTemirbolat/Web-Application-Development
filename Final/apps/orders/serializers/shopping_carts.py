# Python
from typing import Type

from rest_framework.serializers import (
    ModelSerializer,
)

from apps.orders.models import CartItem
from apps.orders.serializers.products import ForeignProductModelSerializer


class BaseCartItemModelSerializer(ModelSerializer):
    """CartItem Base model serializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[CartItem] = CartItem
        fields: str = "__all__"


class ListCartItemProductsModelSerializer(BaseCartItemModelSerializer):
    """Serializer for listing CartItem."""

    product: ForeignProductModelSerializer = ForeignProductModelSerializer()
