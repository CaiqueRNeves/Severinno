"""ViewSets para solicitações de software."""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.exceptions import PermissionDenied

from reservations.models import Reservation
from software_requests.models import SoftwareRequest
from software_requests.permissions import IsAdminOrOwnerReservation
from software_requests.serializers import (
    SoftwareRequestSerializer,
    SoftwareRequestStatusSerializer,
)


class SoftwareRequestViewSet(viewsets.ModelViewSet):
    """Controla o ciclo de vida das solicitações."""

    queryset = SoftwareRequest.objects.select_related("reservation", "reservation__professor", "reservation__room")
    serializer_class = SoftwareRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwnerReservation]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if getattr(user, "user_type", "").upper() == "PROFESSOR":
            reservation_ids = Reservation.objects.filter(professor=user).values_list("id", flat=True)
            qs = qs.filter(reservation_id__in=reservation_ids)
        return qs

    def perform_create(self, serializer):
        reservation = serializer.validated_data["reservation"]
        user = self.request.user
        if getattr(user, "user_type", "").upper() != "ADMIN" and reservation.professor_id != user.id:
            raise PermissionDenied("Você não pode solicitar software para reservas de outros usuários.")
        serializer.save()

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        request_obj = self.get_object()
        if getattr(request.user, "user_type", "").upper() != "ADMIN":
            return Response({"detail": "Apenas administradores podem atualizar o status."}, status=status.HTTP_403_FORBIDDEN)
        serializer = SoftwareRequestStatusSerializer(instance=request_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(SoftwareRequestSerializer(request_obj).data)
