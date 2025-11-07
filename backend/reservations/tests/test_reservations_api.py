"""Testes do módulo de reservas."""

from datetime import date, time, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reservations.models import Reservation
from rooms.models import Room

User = get_user_model()


class ReservationFlowTests(APITestCase):
    """Cobre criação, conflito, cancelamento e disponibilidade."""

    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin-res@severinno.com",
            matricula="ADM-RES",
            password="senha-admin",
            user_type=User.UserType.ADMIN,
        )
        self.professor = User.objects.create_user(
            email="prof-res@severinno.com",
            matricula="PROF-RES",
            password="senha-prof",
            user_type=User.UserType.PROFESSOR,
        )
        self.room = Room.objects.create(
            name="Laboratório de IA",
            code="LABIA",
            location="Bloco D",
            capacity=40,
        )
        self.list_url = reverse("reservation-list")
        self.available_url = reverse("reservation-available")

    def test_professor_creates_and_cancels_reservation(self):
        self.client.force_authenticate(user=self.professor)
        payload = {
            "room": self.room.id,
            "date": (date.today() + timedelta(days=1)).isoformat(),
            "start_time": "10:00",
            "end_time": "12:00",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservation_id = response.data["id"]

        cancel_url = reverse("reservation-cancel", args=[reservation_id])
        cancel_resp = self.client.post(cancel_url, {"confirm": True}, format="json")
        self.assertEqual(cancel_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(cancel_resp.data["status"], Reservation.Status.CANCELLED)

    def test_prevents_overlapping_reservations(self):
        Reservation.objects.create(
            professor=self.professor,
            room=self.room,
            date=date.today() + timedelta(days=2),
            start_time=time(8, 0),
            end_time=time(10, 0),
        )
        self.client.force_authenticate(user=self.professor)
        payload = {
            "room": self.room.id,
            "date": (date.today() + timedelta(days=2)).isoformat(),
            "start_time": "09:00",
            "end_time": "11:00",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_available_endpoint_lists_free_rooms(self):
        other_room = Room.objects.create(name="Sala Livre", code="SALAL", location="Bloco A", capacity=20)
        Reservation.objects.create(
            professor=self.professor,
            room=self.room,
            date=date.today() + timedelta(days=3),
            start_time=time(13, 0),
            end_time=time(15, 0),
        )
        self.client.force_authenticate(user=self.admin)
        params = {
            "date": (date.today() + timedelta(days=3)).isoformat(),
            "start_time": "13:30",
            "end_time": "14:30",
        }
        response = self.client.get(self.available_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        unavailable = next(item for item in response.data if item["room_id"] == self.room.id)
        available = next(item for item in response.data if item["room_id"] == other_room.id)
        self.assertFalse(unavailable["available"])
        self.assertTrue(available["available"])

    def test_cannot_cancel_after_start(self):
        reservation = Reservation.objects.create(
            professor=self.professor,
            room=self.room,
            date=date.today(),
            start_time=time(0, 0),
            end_time=time(1, 0),
        )
        self.client.force_authenticate(user=self.professor)
        cancel_url = reverse("reservation-cancel", args=[reservation.id])
        response = self.client.post(cancel_url, {"confirm": True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
