"""Testes garantindo o comportamento personalizado do Django Admin."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

User = get_user_model()


class AdminDashboardTests(TestCase):
    """Valida branding e CRUD customizado de professores."""

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="admin@severinno.com",
            matricula="ROOT",
            password="senha-admin",
        )
        self.professor = User.objects.create_user(
            email="prof@severinno.com",
            matricula="PROF1",
            password="senha-prof",
            user_type=User.UserType.PROFESSOR,
        )
        self.coordinator = User.objects.create_user(
            email="coordenador@severinno.com",
            matricula="ADM1",
            password="senha-prof",
            user_type=User.UserType.ADMIN,
        )

        self.client.force_login(self.superuser)

    def test_admin_branding_available(self):
        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, "Severinno")
        self.assertContains(response, "Painel administrativo")

    def test_professor_changelist_lists_only_professors(self):
        url = reverse("admin:accounts_professor_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.professor.email)
        self.assertNotContains(response, self.coordinator.email)

    def test_professor_creation_forces_user_type(self):
        url = reverse("admin:accounts_professor_add")
        payload = {
            "email": "novo@severinno.com",
            "matricula": "PROF9",
            "full_name": "Novo Docente",
            "password1": "senha-forte",
            "password2": "senha-forte",
        }
        response = self.client.post(url, payload, follow=True)
        self.assertEqual(response.status_code, 200)
        created = User.objects.get(email=payload["email"])
        self.assertEqual(created.user_type, User.UserType.PROFESSOR)
