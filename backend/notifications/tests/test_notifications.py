"""Testes do módulo de notificações."""

from datetime import date, time, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from notifications.models import Notification
from reservations.models import Reservation
from rooms.models import Room
from software_requests.models import SoftwareRequest

User = get_user_model()


class NotificationTests(APITestCase):
    def setUp(self):
        self.professor = User.objects.create_user(
            email="prof-notify@severinno.com",
            matricula="NTF001",
            password="senha-prof",
            user_type=User.UserType.PROFESSOR,
        )
        self.room = Room.objects.create(name="Lab Notify", code="NTF", location="Bloco N", capacity=15)
        self.client.force_authenticate(user=self.professor)
        self.list_url = reverse("notification-list")

    def test_reservation_creation_generates_notifications(self):
        Reservation.objects.create(
            professor=self.professor,
            room=self.room,
            date=date.today() + timedelta(days=1),
            start_time=time(8, 0),
            end_time=time(10, 0),
        )
        self.assertGreaterEqual(Notification.objects.filter(user=self.professor).count(), 1)

    def test_mark_as_read(self):
        notification = Notification.objects.create(
            user=self.professor,
            title="Teste",
            message="Mensagem",
        )
        url = reverse("notification-mark-as-read", args=[notification.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_software_request_status_update(self):
        reservation = Reservation.objects.create(
            professor=self.professor,
            room=self.room,
            date=date.today() + timedelta(days=2),
            start_time=time(9, 0),
            end_time=time(11, 0),
        )
        request = SoftwareRequest.objects.create(
            reservation=reservation,
            name="VS Code",
        )
        request.status = SoftwareRequest.Status.APPROVED
        request.save()
        self.assertTrue(
            Notification.objects.filter(user=self.professor, related_model="SoftwareRequest").exists()
        )
