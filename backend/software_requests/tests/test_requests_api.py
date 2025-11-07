"""Testes do módulo de solicitações de software."""

from datetime import date, time, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reservations.models import Reservation
from rooms.models import Machine, Room
from software_requests.models import SoftwareRequest

User = get_user_model()


class SoftwareRequestAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin-soft@severinno.com",
            matricula="ADM-SOFT",
            password="senha-admin",
            user_type=User.UserType.ADMIN,
        )
        self.professor = User.objects.create_user(
            email="prof-soft@severinno.com",
            matricula="PRO-SOFT",
            password="senha-prof",
            user_type=User.UserType.PROFESSOR,
        )
        self.other_prof = User.objects.create_user(
            email="outro@severinno.com",
            matricula="OUTRO",
            password="senha-prof",
            user_type=User.UserType.PROFESSOR,
        )
        self.room = Room.objects.create(name="Lab Software", code="LABSW", location="Bloco S", capacity=20)
        self.machine = Machine.objects.create(
            room=self.room,
            processador="Intel i7",
            memoria=16,
            tipo_memoria="DDR4",
            armazenamento="SSD 1TB",
            placa_mae="Dell",
            numero_serie="SW-01",
        )
        self.reservation = Reservation.objects.create(
            professor=self.professor,
            room=self.room,
            date=date.today() + timedelta(days=5),
            start_time=time(9, 0),
            end_time=time(12, 0),
        )
        self.list_url = reverse("software-request-list")

    def test_professor_creates_request_for_own_reservation(self):
        self.client.force_authenticate(user=self.professor)
        payload = {
            "reservation": self.reservation.id,
            "machine": self.machine.id,
            "name": "Matlab",
            "version": "R2024b",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SoftwareRequest.objects.count(), 1)

    def test_professor_cannot_create_for_other_reservation(self):
        other_reservation = Reservation.objects.create(
            professor=self.other_prof,
            room=self.room,
            date=self.reservation.date,
            start_time=time(13, 0),
            end_time=time(15, 0),
        )
        self.client.force_authenticate(user=self.professor)
        payload = {
            "reservation": other_reservation.id,
            "name": "VS Code",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_updates_status(self):
        request_obj = SoftwareRequest.objects.create(
            reservation=self.reservation,
            machine=self.machine,
            name="Docker",
            status=SoftwareRequest.Status.PENDING,
        )
        self.client.force_authenticate(user=self.admin)
        url = reverse("software-request-update-status", args=[request_obj.id])
        response = self.client.patch(
            url,
            {"status": SoftwareRequest.Status.APPROVED},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request_obj.refresh_from_db()
        self.assertEqual(request_obj.status, SoftwareRequest.Status.APPROVED)

    def test_available_in_room_only_machine_from_same_room(self):
        other_room = Room.objects.create(name="Outro Lab", code="LABO", location="Bloco O", capacity=20)
        machine_other = Machine.objects.create(
            room=other_room,
            processador="Ryzen",
            memoria=32,
            tipo_memoria="DDR5",
            armazenamento="SSD 2TB",
            placa_mae="Asus",
            numero_serie="SW-99",
        )
        self.client.force_authenticate(user=self.professor)
        payload = {
            "reservation": self.reservation.id,
            "machine": machine_other.id,
            "name": "Unity",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
