# Python modules
from typing import Any, Type

# DRF
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response as DRFResponse
from rest_framework.request import Request as DRFRequest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_501_NOT_IMPLEMENTED,
)
from rest_framework.permissions import (
    IsAuthenticated,
    BasePermission,
)
from rest_framework.decorators import action

# Django
from django.db.models import QuerySet, F
from django.db.models.manager import BaseManager
from django.db import transaction

# Project
from apps.abstracts.handlers import DRFResponseHandler
from apps.abstracts.decorators import (
    find_queryset_object_by_query_pk,
    validate_serializer_data,
)
from apps.orders.utils import convert_to_int
from apps.orders.models import (
    Order,
    OrderProduct,
    Product,
    CartItem,
    ShoppingCart,
)
from apps.orders.serializers.products import (
    BaseProductModelSerializer,
    ListProductModelSerializer,
)
from apps.orders.serializers.shopping_carts import (
    BaseCartItemModelSerializer,
    ListCartItemProductsModelSerializer,
)
from apps.orders.serializers.reviews import (
    CreateReviewModelSerializer,
    ListReviewModelSerializer,
)
from apps.orders.serializers.orders import BaseOrderModelSerializer
from apps.orders.serializers.payments import CreatePaymentModelSerializer


class ProductViewSet(DRFResponseHandler, ViewSet):
    """Product View set."""

    queryset: BaseManager[Product] = Product.objects
    permission_classes: tuple[BasePermission] = (IsAuthenticated,)
    serializer_class: Type[BaseProductModelSerializer] = BaseProductModelSerializer

    def get_queryset(self) -> QuerySet[Product]:
        """Get product queryset."""

        return self.queryset.all()

    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle GET-request to view all products."""

        return self.get_drf_response(
            request=request,
            data=self.get_queryset().select_related("category"),
            serializer_class=ListProductModelSerializer,
            many=True
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="add-review",
        url_name="add_review",
    )
    @validate_serializer_data(
        serializer_class=CreateReviewModelSerializer
    )
    def add_review(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle POST request to add a review for a product."""
        serializer: CreateReviewModelSerializer = kwargs["serializer"]

        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )

    @action(
        methods=["GET"],
        detail=True,
        url_path="view-reviews",
        url_name="view_reviews",
    )
    @find_queryset_object_by_query_pk(
        queryset=Product.objects,
        class_name=Product,
        entity_name="Product"
    )
    def get_reviews(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        product: Product = kwargs["object"]

        return self.get_drf_response(
            request=request,
            data=product.reviews.select_related("user").all(),
            serializer_class=ListReviewModelSerializer,
            many=True
        )


class ShoppingCartViewSet(DRFResponseHandler, ViewSet):
    """Shopping cart view set for all the endpoints."""

    queryset: BaseManager[Product] = ShoppingCart.objects
    permission_classes: tuple[BasePermission] = (IsAuthenticated,)
    serializer_class: Type[BaseCartItemModelSerializer] = BaseCartItemModelSerializer

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
        methods=["GET"],
        detail=False,
        url_path="cart-products",
        url_name="cart_products",
    )
    def get_cart_products(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle GET-request to view all the products in the cart."""
        cart_items: QuerySet[CartItem] = CartItem.objects.filter(
            cart=request.user.shopping_cart
        ).select_related(
            "product"
        )
        return self.get_drf_response(
            request=request,
            data=cart_items,
            serializer_class=ListCartItemProductsModelSerializer,
            many=True
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="add-product",
        url_name="add_product",
    )
    @find_queryset_object_by_query_pk(
        queryset=ShoppingCart.objects,
        class_name=ShoppingCart,
        entity_name="Shopping cart"
    )
    def add_product(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle POST request to add a new product."""
        cart: ShoppingCart = kwargs["object"]

        product: bool = Product.objects.filter(
            id=request.data.get("product", -1)
        ).exists()
        if not product:
            return DRFResponse(
                data={
                    "product": [
                        f"There is no such product with PK {product}"
                    ]
                },
                status=HTTP_404_NOT_FOUND
            )

        cart_item_exist: bool = CartItem.objects.filter(
            cart=cart,
            product=request.data.get("product")
        ).exists()

        if cart_item_exist:
            CartItem.objects.filter(
                cart=cart,
                product=request.data.get("product")
            ).update(
                quantity=F("quantity") + convert_to_int(request.data.get("quantity", 1))
            )
        else:
            CartItem.objects.create(
                cart=cart,
                product=request.data.get("product"),
                quantity=1
            )
        return DRFResponse(status=HTTP_200_OK)

    @action(
        methods=["DELETE"],
        detail=True,
        url_path="remove-product",
        url_name="remove_product",
    )
    @find_queryset_object_by_query_pk(
        queryset=ShoppingCart.objects,
        class_name=ShoppingCart,
        entity_name="Shopping cart"
    )
    def remove_product(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle DELETE request to remove a product from the cart."""

        cart: ShoppingCart = kwargs["object"]

        product: bool = Product.objects.filter(
            id=request.data.get("product", -1)
        ).exists()
        if not product:
            return DRFResponse(
                data={
                    "product": [
                        f"There is no such product with PK {product}"
                    ]
                },
                status=HTTP_404_NOT_FOUND
            )

        CartItem.objects.filter(
            cart=cart,
            product=request.data.get("product")
        ).delete()
        return DRFResponse(status=HTTP_204_NO_CONTENT)


class OrderViewSet(DRFResponseHandler, ViewSet):
    """Order related endpoints."""

    queryset: BaseManager[Order] = Order.objects
    permission_classes: tuple[BasePermission] = (IsAuthenticated,)
    serializer_class: Type[BaseOrderModelSerializer] = BaseOrderModelSerializer

    def create(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle POST-request to create a new order."""

        cart_items: QuerySet[CartItem] = CartItem.objects.select_related(
            "product"
        ).filter(
            cart=request.user.shopping_cart
        )

        if not cart_items.exists():
            return DRFResponse(
                data="You have no items in your cart",
                status=HTTP_400_BAD_REQUEST
            )

        total_price: int = 0

        item: CartItem
        for item in cart_items:
            total_price += item.product.price * item.quantity


        with transaction.atomic():
            order: Order = Order.objects.create(
                purchaser=request.user,
                total_price=total_price
            )

            order_products: list[OrderProduct] = [
                OrderProduct(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=int(item.quantity*item.product.price)
                )
                for item in cart_items
            ]
            OrderProduct.objects.bulk_create(order_products)

            # Commit the changes only if everything is successful
            # Clear the cart after the order is placed
            cart_items.delete()

        return DRFResponse(status=HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="pay",
        url_name="pay",
    )
    @find_queryset_object_by_query_pk(
        queryset=Order.objects,
        class_name=Order,
        entity_name="Order"
    )
    def pay(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle POST-request to create an order."""

        order: Order = kwargs["object"]
        data_copy: dict[str, Any] = request.data.copy()
        data_copy["order"] = order.id
        data_copy["amount"] = order.total_price
        serializer: CreatePaymentModelSerializer = CreatePaymentModelSerializer(
            data=data_copy
        )
        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )



