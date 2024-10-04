from typing import (
    Any,
    Callable,
    Type,
)
from functools import wraps

from rest_framework.serializers import Serializer
from rest_framework.request import Request as DRFRequest
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response as DRFResponse


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
