from django.db.models import (
    DateTimeField,
    Model,
)


class AbstractBaseModel(Model):
    """
    AbstractBaseModel database model, holding data we need for every model
    in the different apps.
    """

    created_at: DateTimeField = DateTimeField(
        auto_now_add=True, verbose_name="Date and time of creation"
    )
    updated_at: DateTimeField = DateTimeField(
        auto_now=True,
        verbose_name="Date and time of last update",
    )

    class Meta:
        """Customization of the table view."""

        abstract: bool = True
