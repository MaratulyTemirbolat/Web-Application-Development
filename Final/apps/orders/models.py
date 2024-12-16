# Python
from typing import Optional

# Django
from django.core.validators import MaxValueValidator
from django.db.models import (
    CharField,
    TextField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    URLField,
    IntegerField,
    ManyToManyField,
    Model,
    ForeignKey,
    OneToOneField,
    BaseConstraint,
    UniqueConstraint,
    CASCADE,
)

# Django
from django.contrib.auth.models import User

# Project
from apps.abstracts.models import AbstractBaseModel


class Category(AbstractBaseModel):
    """Category database model."""

    NAME_MAX_LEN = 100

    name: str = CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
        db_index=True,
        verbose_name="Category name",
    )

    class Meta:
        """Customization of the Table."""

        ordering: tuple[str] = ("-updated_at",)
        verbose_name: str = "Category"
        verbose_name_plural: str = "Categories"

    def __str__(self) -> str:
        """Override category instance print result."""
        return self.name


class Product(AbstractBaseModel):
    """Product database model."""

    NAME_MAX_LEN = 254
    PHOTO_URL_MAX_LEN = 254

    name: str = CharField(
        max_length=NAME_MAX_LEN,
        verbose_name="Name of the product"
    )
    description: str = TextField(
        verbose_name="Product's description"
    )
    price: int = PositiveIntegerField(
        verbose_name="Product's price"
    )
    photo_url: str = URLField(
        max_length=PHOTO_URL_MAX_LEN,
        verbose_name="Photo URL"
    )
    category: Category = ForeignKey(
        to=Category,
        on_delete=CASCADE,
        related_name="products",
        verbose_name="Product's category"
    )

    class Meta:
        """Customization of the Table."""

        ordering: tuple[str] = ("-updated_at",)
        verbose_name: str = "Product"
        verbose_name_plural: str = "Products"

    def __str__(self) -> str:
        """Override default product instance print result."""
        return self.name


class Order(AbstractBaseModel):
    """Order database model."""

    STATUS_PENDING = 0
    STATUS_PENDING_TEXT = "Pending"
    STATUS_ACCEPTED = 1
    STATUS_ACCEPTED_TEXT = "Accepted"
    STATUS_ON_THE_WAY = 2
    STATUS_ON_THE_WAY_TEXT = "On the way"
    STATUS_CLOSED = 3
    STATUS_CLOSED_TEXT = "Closed"
    STATUS_CHOICES = (
        (STATUS_PENDING, STATUS_PENDING_TEXT),
        (STATUS_ACCEPTED, STATUS_ACCEPTED_TEXT),
        (STATUS_ON_THE_WAY, STATUS_ON_THE_WAY_TEXT),
        (STATUS_CLOSED, STATUS_CLOSED_TEXT),
    )

    purchaser: User = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="orders",
        verbose_name="Purchaser"
    )
    total_price: int = PositiveIntegerField(
        verbose_name="Final price for the order"
    )
    status: int = IntegerField(
        choices=STATUS_CHOICES,
        verbose_name="Order status "
    )
    products: ManyToManyField = ManyToManyField(
        to=Product,
        related_name="orders",
        through="OrderProduct",
        through_fields=(
            "order",
            "product",
        ),
        blank=True,
        verbose_name="Products"
    )

    class Meta:
        """Customization of the Table."""

        ordering: tuple[str] = ("-updated_at",)
        verbose_name: str = "Order"
        verbose_name_plural: str = "Orders"


class OrderProduct(Model):
    """Order Products database model."""

    order: Order = ForeignKey(
        to=Order,
        on_delete=CASCADE,
        related_name="order_products",
        verbose_name="Order"
    )
    product: Product = ForeignKey(
        to=Product,
        on_delete=CASCADE,
        related_name="order_products",
        verbose_name="Product"
    )
    quantity: int = PositiveSmallIntegerField(
        verbose_name="Number of products"
    )
    price: int = PositiveIntegerField(
        verbose_name="Price for all the products"
    )

    class Meta:
        """Customization of the Table."""

        ordering: tuple[str] = ("-id",)
        verbose_name: str = "Order's product"
        verbose_name_plural: str = "Orders' products"
        constraints: list[BaseConstraint] = [
            UniqueConstraint(
                fields=(
                    "order",
                    "product",
                ),
                name="unique_order_product",
            ),
        ]


class ShoppingCart(AbstractBaseModel):
    """Shoppoing cart database model."""

    user: User = OneToOneField(
        to=User,
        on_delete=CASCADE,
        related_name="shopping_cart",
        verbose_name="Owner"
    )
    products: ManyToManyField = ManyToManyField(
        to=Product,
        related_name="belonged_shopping_carts",
        through="CartItem",
        through_fields=(
            "cart",
            "product",
        ),
        blank=True,
        verbose_name="Products"
    )

    class Meta:
        """Customization of the Table."""

        verbose_name: str = "Shopping cart"
        verbose_name_plural: str = "Shopping carts"
        ordering: tuple[str] = ("-updated_at",)


class CartItem(Model):
    """Cart Item database model."""

    cart: ShoppingCart = ForeignKey(
        to=ShoppingCart,
        on_delete=CASCADE,
        related_name="cart_items",
        verbose_name="Cart"
    )
    product: Product = ForeignKey(
        to=Product,
        on_delete=CASCADE,
        related_name="cart_items",
        verbose_name="Product"
    )
    quantity: int = PositiveSmallIntegerField(
        verbose_name="Quantity"
    )

    class Meta:
        """Customization of the table."""

        ordering: tuple[str] = ("-id",)
        verbose_name: str = "Cart item"
        verbose_name_plural: str = "Carts items"
        constraints: list[BaseConstraint] = [
            UniqueConstraint(
                fields=(
                    "cart",
                    "product",
                ),
                name="unique_cart_product",
            ),
        ]


class State(AbstractBaseModel):
    """State database model."""

    NAME_MAX_LEN = 150

    name: str = CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
        verbose_name="State's name"
    )

    class Meta:
        """Customization of the Table."""

        ordering: tuple[str] = ("-updated_at",)
        verbose_name: str = "State"
        verbose_name_plural: str = "States"

    def __str__(self) -> str:
        """Override instance view with print."""
        return self.name


class City(AbstractBaseModel):
    """City database model."""

    NAME_MAX_LEN = 150

    name: str = CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
        verbose_name="City's name"
    )
    state: State = ForeignKey(
        to=State,
        on_delete=CASCADE,
        related_name="cities",
        verbose_name="State"
    )

    class Meta:
        """Customization of the Table."""

        ordering: tuple[str] = ("-updated_at",)
        verbose_name: str = "City"
        verbose_name_plural: str = "Cities"

    def __str__(self) -> str:
        """Override instance view with print."""
        return self.name


class UserAddress(AbstractBaseModel):
    """User Address database model."""

    STREET_NAME_MAX_LEN = 200
    ZIP_CODE_MAX_LEN = 10

    city: City = ForeignKey(
        to=City,
        on_delete=CASCADE,
        related_name="addresses",
        verbose_name="City"
    )
    street_name: str = CharField(
        max_length=STREET_NAME_MAX_LEN,
        verbose_name="Street name"
    )
    zip_code: str = CharField(
        max_length=ZIP_CODE_MAX_LEN,
        verbose_name="ZIP code"
    )
    user: User = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="addresses",
        verbose_name="User who lives here"
    )


class Review(AbstractBaseModel):
    """Review database model."""

    RATING_MAX_VALUE = 5

    product: Product = ForeignKey(
        to=Product,
        on_delete=CASCADE,
        related_name="reviews",
        verbose_name="Reviewed product"
    )
    user: User = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="reviews",
        verbose_name="User who left review"
    )
    rating: int = PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                limit_value=RATING_MAX_VALUE,
                message=f"Max rating cannot exceed {RATING_MAX_VALUE} stars"
            )
        ],
    )
    comment: Optional[str] = TextField(
        blank=True,
        null=True,
        verbose_name="User's left comment"
    )

    class Meta:
        """Customization of the Table."""

        ordering: tuple[str] = ("-updated_at",)
        verbose_name: str = "Review"
        verbose_name_plural: str = "Reviews"


class Payment(AbstractBaseModel):
    """Payment database model."""

    PAYMENT_METHOD_CASH = 0
    PAYMENT_METHOD_CASH_STR = "Cash"
    PAYMENT_METHOD_CARD = 1
    PAYMENT_METHOD_CARD_STR = "Card"
    PAYMENT_METHODS = (
        (PAYMENT_METHOD_CASH, PAYMENT_METHOD_CASH_STR),
        (PAYMENT_METHOD_CARD, PAYMENT_METHOD_CARD_STR),
    )

    order: Order = OneToOneField(
        to=Order,
        on_delete=CASCADE,
        related_name="payment",
        verbose_name="Order"
    )
    amount: int = PositiveIntegerField(
        verbose_name="Total sum"
    )
    payment_method: int = IntegerField(
        choices=PAYMENT_METHODS,
        verbose_name="Payment method"
    )

    class Meta:
        """Customization of the Table."""

        ordering: tuple[str] = ("-updated_at",)
        verbose_name: str = "Payment"
        verbose_name_plural: str = "Payments"
