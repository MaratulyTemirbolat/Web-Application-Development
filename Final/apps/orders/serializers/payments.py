from typing import Type

from rest_framework.serializers import ModelSerializer

from apps.orders.models import Payment


class BasePaymentModelSerializer(ModelSerializer):
    """Base order model serializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Payment] = Payment
        fields: str = "__all__"


class CreatePaymentModelSerializer(BasePaymentModelSerializer):
    """Create order model serializer."""

    ...
