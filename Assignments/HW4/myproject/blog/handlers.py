from typing import (
    Any,
    Optional,
    Type,
)

from django.db.models import Manager, QuerySet

from rest_framework.pagination import BasePagination
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK


class DRFResponseHandler:
    """Handler for DRF response."""

    def get_drf_response(
        self,
        request: DRFRequest,
        data: QuerySet | Manager,
        serializer_class: Type[Serializer],
        many: bool = False,
        paginator: Optional[BasePagination] = None,
        serializer_context: Optional[dict[str, Any]] = None,
        extra_data: dict[str, Any] = {},
        status_code: int = HTTP_200_OK,
    ) -> DRFResponse:
        """Handler for DRF responses wrapping."""
        if not serializer_context:
            serializer_context: dict[str, Any] = {"request": request}

        if extra_data:
            assert isinstance(extra_data, dict), "'extra_data' must be a dictionary."

        if paginator and many:
            objects: list = paginator.paginate_queryset(
                queryset=data, request=request
            )
            return paginator.get_paginated_response(
                data={
                    **extra_data,
                    "count": paginator.page.paginator.count,
                    "results": serializer_class(
                        objects,
                        many=many,
                        context=serializer_context
                    ).data
                }
            )

        return DRFResponse(
            data=serializer_class(
                data,
                many=many,
                context=serializer_context
            ).data if not extra_data else {
                **extra_data,
                "results": serializer_class(
                    data,
                    many=many,
                    context=serializer_context
                ).data
            },
            status=status_code
        )
