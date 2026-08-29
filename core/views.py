import logging

from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(_request: Request) -> Response:
    try:
        connection.ensure_connection()
        return Response(
            {"status": "healthy", "database": "connected"},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.error("Health check failed - DB error: %s", e, exc_info=True)

        return Response(
            {"status": "unhealthy", "database": "unavailable"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
