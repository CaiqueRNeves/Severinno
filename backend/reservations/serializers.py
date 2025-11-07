"""Serializers responsáveis pelas reservas."""

from django.utils import timezone
from rest_framework import serializers

from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    """Controla criação de reservas com validações avançadas."""

    professor_email = serializers.EmailField(source="professor.email", read_only=True)
    room_name = serializers.CharField(source="room.name", read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "professor",
            "professor_email",
            "room",
            "room_name",
            "date",
            "start_time",
            "end_time",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status", "created_at", "updated_at", "professor_email", "room_name")
        extra_kwargs = {"professor": {"required": False}}

    def validate(self, attrs):
        data = {
            "professor": attrs.get("professor", getattr(self.instance, "professor", None)),
            "room": attrs.get("room", getattr(self.instance, "room", None)),
            "date": attrs.get("date", getattr(self.instance, "date", None)),
            "start_time": attrs.get("start_time", getattr(self.instance, "start_time", None)),
            "end_time": attrs.get("end_time", getattr(self.instance, "end_time", None)),
        }
        temp = Reservation(**data)
        temp.pk = getattr(self.instance, "pk", None)
        try:
            temp.clean()
        except Exception as exc:  # ValidationError
            raise serializers.ValidationError(
                exc.message_dict if hasattr(exc, "message_dict") else exc.messages
            )
        return attrs

    def create(self, validated_data):
        return Reservation.objects.create(**validated_data)


class CancelReservationSerializer(serializers.Serializer):
    """Serializer simples apenas para validar ação de cancelamento."""

    confirm = serializers.BooleanField(default=True)

    def validate(self, attrs):
        reservation: Reservation = self.context["reservation"]
        if reservation.status == Reservation.Status.CANCELLED:
            raise serializers.ValidationError("Esta reserva já foi cancelada.")
        if not reservation.can_cancel():
            raise serializers.ValidationError("O horário já foi atingido; não é possível cancelar.")
        return attrs
