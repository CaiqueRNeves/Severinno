"""Testes garantindo que os signals e API de logs funcionam."""

from datetime import date, time, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from logs.models import AuditLog
from reservations.models import Reservation
from rooms.models import Room
from software_requests.models import SoftwareRequest

User = get_user_model()


class AuditLogTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="auditor@severinno.com",
            matricula="AUD001",
            password="senha-admin",
            user_type=User.UserType.ADMIN,
        )
        self.professor = User.objects.create_user(
            email="prof-log@severinno.com",
            matricula="PROFLOG",
            password="senha-prof",
            user_type=User.UserType.PROFESSOR,
        )
        self.client.force_authenticate(user=self.admin)
        self.logs_url = reverse("audit-log-list")

    def test_reservation_creates_log(self):
        room = Room.objects.create(name="Lab Log", code="LOG1", location="Bloco L", capacity=10)
        Reservation.objects.create(
            professor=self.professor,
            room=room,
            date=date.today() + timedelta(days=1),
            start_time=time(9, 0),
            end_time=time(11, 0),
        )
        self.assertTrue(AuditLog.objects.filter(model="Reservation").exists())

    def test_logs_api_requires_admin(self):
        response = self.client.get(self.logs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.professor)
        response_prof = self.client.get(self.logs_url)
        self.assertEqual(response_prof.status_code, status.HTTP_403_FORBIDDEN)

    def test_software_request_logged(self):
        room = Room.objects.create(name="Lab SW", code="LGSW", location="Bloco S", capacity=10)
        reservation = Reservation.objects.create(
            professor=self.professor,
            room=room,
            date=date.today() + timedelta(days=2),
            start_time=time(8, 0),
            end_time=time(10, 0),
        )
        SoftwareRequest.objects.create(
            reservation=reservation,
            name="Postman",
        )
        self.assertTrue(AuditLog.objects.filter(model="SoftwareRequest").exists())
