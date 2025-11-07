"""ViewSets das reservas com regras de disponibilidade."""

from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reservations.models import Reservation
from reservations.permissions import IsOwnerOrAdmin, IsProfessorOrAdmin
from reservations.serializers import (
    CancelReservationSerializer,
    ReservationSerializer,
)
from rooms.models import Room


class ReservationViewSet(viewsets.ModelViewSet):
    """Endpoint principal para reservas de salas."""

    serializer_class = ReservationSerializer
    queryset = Reservation.objects.select_related("room", "professor")
    permission_classes = [IsProfessorOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if getattr(user, "user_type", "").upper() == "PROFESSOR":
            return qs.filter(professor=user)
        return qs

    def get_permissions(self):
        permissions = [permission() for permission in self.permission_classes]
        if self.action in {"retrieve", "update", "partial_update", "destroy", "cancel"}:
            permissions.append(IsOwnerOrAdmin())
        return permissions

    def perform_create(self, serializer):
        professor = serializer.validated_data.get("professor") or self.request.user
        serializer.save(professor=professor)

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Utilize o endpoint de cancelamento.")

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        serializer = CancelReservationSerializer(data=request.data, context={"reservation": reservation})
        serializer.is_valid(raise_exception=True)
        reservation.cancel()
        return Response(ReservationSerializer(reservation).data)

    @action(detail=False, methods=["get"], url_path="available")
    def available(self, request):
        """Retorna salas disponíveis para o intervalo informado."""

        date_str = request.query_params.get("date")
        start_str = request.query_params.get("start_time")
        end_str = request.query_params.get("end_time")
        if not all([date_str, start_str, end_str]):
            return Response(
                {"detail": "Informe date, start_time e end_time."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_str, "%H:%M").time()
            end_time = datetime.strptime(end_str, "%H:%M").time()
        except ValueError:
            return Response({"detail": "Formato inválido. Use YYYY-MM-DD e HH:MM."}, status=400)

        rooms = Room.objects.filter(is_active=True).order_by("name")
        available = []
        for room in rooms:
            conflict = Reservation.objects.active().filter(
                room=room,
                date=date_obj,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exists()
            available.append(
                {
                    "room_id": room.id,
                    "room_name": room.name,
                    "room_code": room.code,
                    "available": not conflict,
                }
            )
        return Response(available)
