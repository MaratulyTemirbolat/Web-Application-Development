from typing import (
    Any,
    Optional,
    Type,
)

from django.db.models import Manager, QuerySet

from rest_framework.pagination import BasePagination
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.serializers import Serializer
from rest_framework.status import (
    HTTP_200_OK,
)


class DRFResponseHandler:
    """Handler for DRF response."""

    def get_drf_response(
        self,
        request: DRF_Request,
        data: QuerySet | Manager,
        serializer_class: Type[Serializer],
        many: bool = False,
        paginator: Optional[BasePagination] = None,
        serializer_context: Optional[dict[str, Any]] = None,
        status_code: int = HTTP_200_OK,
    ) -> DRF_Response:
        if not serializer_context:
            serializer_context = {"request": request}
        if paginator and many:
            objects: list = paginator.paginate_queryset(
                queryset=data, request=request
            )
            serializer: Serializer = serializer_class(
                objects, many=many, context=serializer_context
            )
            response: DRF_Response = paginator.get_paginated_response(
                serializer.data
            )
            return response

        serializer: Serializer = serializer_class(
            data, many=many, context=serializer_context
        )
        response: DRF_Response = DRF_Response(
            {'response': serializer.data}, status=status_code
        )
        return response

    def get_simple_drf_response(
        self,
        data: Any,
        status_code: int = HTTP_200_OK,
    ) -> DRF_Response:
        """Method to return DRF response with applied data and status code."""
        return DRF_Response(
            data={"response": data},
            status=status_code,
        )
