"""Serializers para as entidades de salas e máquinas."""

from django.utils import timezone
from rest_framework import serializers

from rooms.models import Machine, Room


class MachineSerializer(serializers.ModelSerializer):
    """Serializa máquinas com todas as especificações."""

    room_name = serializers.CharField(source="room.name", read_only=True)
    room_code = serializers.CharField(source="room.code", read_only=True)

    class Meta:
        model = Machine
        fields = (
            "id",
            "room",
            "room_name",
            "room_code",
            "hostname",
            "processador",
            "memoria",
            "tipo_memoria",
            "armazenamento",
            "placa_mae",
            "numero_serie",
            "observacoes",
            "is_available",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class RoomSerializer(serializers.ModelSerializer):
    """Serializa salas e agrega máquinas cadastradas."""

    machines = MachineSerializer(many=True, read_only=True)
    is_available_now = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "code",
            "location",
            "capacity",
            "description",
            "is_active",
            "is_available_now",
            "created_at",
            "updated_at",
            "machines",
        )
        read_only_fields = ("created_at", "updated_at")

    @staticmethod
    def get_is_available_now(obj):
        now = timezone.localtime()
        return not obj.reservations.active().filter(
            date=now.date(),
            start_time__lte=now.time(),
            end_time__gte=now.time(),
        ).exists()
