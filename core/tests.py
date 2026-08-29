from typing import override
from unittest.mock import MagicMock, patch

from django.db import OperationalError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    url: str = ""

    @override
    def setUp(self):
        self.url = reverse("health-check")

    def test_health_check_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {"status": "healthy", "database": "connected"},
        )

    @patch("core.views.logger.error")
    @patch("core.views.connection.ensure_connection")
    def test_health_check_database_failure(
        self, mock_ensure_connection: MagicMock, mock_logger_error: MagicMock
    ):
        mock_ensure_connection.side_effect = OperationalError("DB connection error")
        mock_logger_error.return_value = None

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(
            response.json(),
            {"status": "unhealthy", "database": "unavailable"},
        )
        mock_logger_error.assert_called_once()
