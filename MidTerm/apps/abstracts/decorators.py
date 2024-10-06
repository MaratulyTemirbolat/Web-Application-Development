from typing import (
    Any,
    Callable,
    Type,
    TypeVar,
    Optional,
)
from functools import wraps

from django.db.models import QuerySet, Manager

from rest_framework.serializers import Serializer
from rest_framework.request import Request as DRFRequest
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.response import Response as DRFResponse



T = TypeVar("T")


def validate_serializer_data(
    serializer_class: Type[Serializer],
    context: dict[str, Any] = {},
    check_query_params: bool = False,
) -> Callable:
    """Decorator to preprocess the request data for SAS credentials."""

    def decorator(
        func: Callable[
            [DRFRequest, tuple[Any, ...], dict[Any, Any]], DRFResponse
        ],
    ) -> Callable:
        @wraps(func)
        def wrapper(
            request: DRFRequest | Any,
            *args: tuple[Any, ...],
            **kwargs: dict[Any, Any],
        ):
            # Get the serializer's validated data and check
            req: Any = request

            if not isinstance(request, DRFRequest):
                for arg in args:
                    if isinstance(arg, DRFRequest):
                        req = arg
                        break

            if not "request" in context:
                context["request"] = req

            serializer: Serializer = serializer_class(
                data=req.query_params
                if check_query_params
                else req.data,
                context=context,
            )
            if serializer.is_valid():
                kwargs["validated_data"] = serializer.validated_data.copy()
                kwargs["serializer"] = serializer
                return func(req, *args, **kwargs)
            else:
                return DRFResponse(
                    data=serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )

        return wrapper

    return decorator


def find_queryset_object_by_query_pk(
    queryset: QuerySet[T] | Manager[T],
    class_name: Type[T],
    entity_name: str,
) -> Callable:
    """
    Decorator to find an object by its primary key in the queryset.

    - queryset: The queryset or class manager to search for the object.
    - class_name: The class name of the model.
    - entity_name: The name of the entity which will be used in the error message.
    """

    def decorator(
        func: Callable[
            [DRFRequest, tuple[Any, ...], dict[Any, Any]], DRFResponse
        ],
    ) -> Callable:
        @wraps(func)
        def wrapper(
            request: DRFRequest,
            *args: tuple[Any, ...],
            **kwargs: dict[Any, Any],
        ) -> DRFResponse:
            """Get the object from the queryset and pass it to the view. If the object is not found, return a 404 response."""
            pk: Optional[str] = kwargs.get("pk", None)
            assert pk is not None, "Primary key is not provided"
            try:
                kwargs["object"] = queryset.get(pk=pk)
                return func(request, *args, **kwargs)
            except class_name.DoesNotExist:
                return DRFResponse(
                    data={
                        "id": [
                            f"The {entity_name} with id {pk} has not been found"
                        ]
                    },
                    status=HTTP_404_NOT_FOUND,
                )

        return wrapper

    return decorator
