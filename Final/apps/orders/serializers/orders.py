from typing import Type

from rest_framework.serializers import (
    ModelSerializer,
    HiddenField,
    CurrentUserDefault,
)

from apps.orders.models import Order, OrderProduct


class BaseOrderModelSerializer(ModelSerializer):
    """Base order model serializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Order] = Order
        fields: str = "__all__"


class CreateOrderModelSerializer(BaseOrderModelSerializer):
    """Create order model serializer."""

    purchaser: HiddenField = HiddenField(default=CurrentUserDefault())


class BaseOrderProductModelSerializer(ModelSerializer):
    """Base order product model serializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[OrderProduct] = OrderProduct
        fields: str = "__all__"


class CreateOrderProductModelSerializer(BaseOrderProductModelSerializer):
    """Create order product model serializer."""

    ...
