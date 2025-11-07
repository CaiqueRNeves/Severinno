"""Testes dos fluxos de autenticação JWT."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationFlowTests(APITestCase):
    """Cobre cadastro, login, refresh e acesso autenticado."""

    def setUp(self):
        self.register_url = reverse("accounts-register")
        self.login_url = reverse("accounts-login")
        self.refresh_url = reverse("accounts-refresh")
        self.profile_url = reverse("accounts-profile")

    def test_register_creates_user(self):
        payload = {
            "email": "docente@example.com",
            "matricula": "TST123",
            "password": "senha-super-segura",
            "user_type": User.UserType.PROFESSOR,
        }
        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=payload["email"]).exists())

    def test_login_and_profile_flow(self):
        user = User.objects.create_user(
            email="admin@example.com",
            matricula="ADM001",
            password="senha-admin",
            user_type=User.UserType.ADMIN,
        )

        login_response = self.client.post(
            self.login_url,
            {"email": user.email, "password": "senha-admin"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access = login_response.data["access"]
        refresh = login_response.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        profile_response = self.client.get(self.profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["email"], user.email)

        refresh_response = self.client.post(
            self.refresh_url,
            {"refresh": refresh},
            format="json",
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)
