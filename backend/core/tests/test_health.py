"""Testes do endpoint de saúde da API."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckViewTests(APITestCase):
    """Garantem que o health check responda conforme esperado."""

    def test_health_endpoint_returns_ok_status(self):
        """Deve retornar HTTP 200 com o payload mínimo esperado."""

        url = reverse("health-check")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "ok")
        self.assertIn("timestamp", response.data)
        self.assertIn("ambiente", response.data)
