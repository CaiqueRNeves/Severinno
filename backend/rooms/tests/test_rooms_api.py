"""Testes de API para o módulo de salas e máquinas."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rooms.models import Machine, Room

User = get_user_model()


class RoomsPermissionsTests(APITestCase):
    """Garante que apenas administradores possam manipular recursos."""

    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin-rooms@severinno.com",
            matricula="ADMROOM",
            password="senha-admin",
            user_type=User.UserType.ADMIN,
        )
        self.professor = User.objects.create_user(
            email="prof-rooms@severinno.com",
            matricula="PROOM",
            password="senha-prof",
            user_type=User.UserType.PROFESSOR,
        )
        self.rooms_url = reverse("room-list")
        self.machines_url = reverse("machine-list")

    def test_professor_cannot_create_room(self):
        self.client.force_authenticate(user=self.professor)
        payload = {
            "name": "Lab Segurança",
            "code": "LABSEC",
            "location": "Bloco C",
            "capacity": 30,
        }
        response = self.client.post(self.rooms_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_creates_room_and_machine(self):
        self.client.force_authenticate(user=self.admin)
        room_payload = {
            "name": "Laboratório de Redes",
            "code": "LABRED",
            "location": "Bloco B 201",
            "capacity": 25,
        }
        room_response = self.client.post(self.rooms_url, room_payload, format="json")
        self.assertEqual(room_response.status_code, status.HTTP_201_CREATED)
        room_id = room_response.data["id"]

        machine_payload = {
            "room": room_id,
            "hostname": "pc-redes-01",
            "processador": "Intel i5",
            "memoria": 16,
            "tipo_memoria": "DDR4",
            "armazenamento": "SSD 480GB",
            "placa_mae": "ASUS Prime",
            "numero_serie": "SN-001",
            "observacoes": "Uso em aulas práticas.",
        }
        machine_response = self.client.post(self.machines_url, machine_payload, format="json")
        self.assertEqual(machine_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Machine.objects.count(), 1)

        detail_response = self.client.get(reverse("room-detail", args=[room_id]))
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(detail_response.data["machines"]), 1)

    def test_serial_number_must_be_unique(self):
        self.client.force_authenticate(user=self.admin)
        room = Room.objects.create(name="Sala 1", code="S1", location="Bloco A", capacity=10)
        Machine.objects.create(
            room=room,
            processador="Ryzen 5",
            memoria=16,
            tipo_memoria="DDR4",
            armazenamento="SSD 500GB",
            placa_mae="Gigabyte",
            numero_serie="SERIAL-1",
        )
        payload = {
            "room": room.id,
            "processador": "Ryzen 7",
            "memoria": 32,
            "tipo_memoria": "DDR5",
            "armazenamento": "SSD 1TB",
            "placa_mae": "MSI",
            "numero_serie": "SERIAL-1",
        }
        response = self.client.post(self.machines_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("numero_serie", response.data)
