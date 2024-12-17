from django.contrib.admin import (
    ModelAdmin,
    register
)

from apps.orders.models import (
    Category,
    Product,
    Order,
    OrderProduct,
    ShoppingCart,
    CartItem,
    State,
    City,
    UserAddress,
    Review,
    Payment,
)


@register(Category)
class CategoryAdmin(ModelAdmin):
    """Category admin model."""

    ...


@register(Product)
class ProductAdmin(ModelAdmin):
    """Product admin model."""

    ...


@register(Order)
class OrderAdmin(ModelAdmin):
    """Order admin model."""

    ...


@register(OrderProduct)
class OrderProductAdmin(ModelAdmin):
    """OrderProduct admin model."""

    ...


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    """ShoppingCart admin model."""

    ...


@register(CartItem)
class CartItemAdmin(ModelAdmin):
    """CartItem admin model."""

    ...


@register(State)
class StateAdmin(ModelAdmin):
    """State admin model."""

    ...


@register(City)
class CityAdmin(ModelAdmin):
    """City admin model."""

    ...


@register(UserAddress)
class UserAddressAdmin(ModelAdmin):
    """UserAddress admin model."""

    ...


@register(Review)
class ReviewAdmin(ModelAdmin):
    """Review admin model."""

    ...


@register(Payment)
class PaymentAdmin(ModelAdmin):
    """Payment admin model."""

    ...
