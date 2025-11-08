"""Testes do endpoint de logs."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from logs.models import AuditLog

User = get_user_model()


class AuditLogAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin-logapi@severinno.com",
            matricula="ADMLOG",
            password="senha-admin",
            user_type=User.UserType.ADMIN,
        )
        self.actor = User.objects.create_user(
            email="actor@severinno.com",
            matricula="ACT1",
            password="senha",
            user_type=User.UserType.PROFESSOR,
        )
        AuditLog.objects.create(
            actor=self.actor,
            action="LOGIN",
            model="User",
            object_id=str(self.actor.id),
            description="Usuário realizou login.",
        )
        self.url = reverse("audit-log-list")

    def test_admin_can_retrieve_logs(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_non_admin_cannot_retrieve(self):
        self.client.force_authenticate(user=self.actor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
