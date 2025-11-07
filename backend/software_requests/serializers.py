"""Serializers para solicitações de software."""

from rest_framework import serializers

from software_requests.models import SoftwareRequest


class SoftwareRequestSerializer(serializers.ModelSerializer):
    """Serializer principal com validações e transições de status."""

    professor_email = serializers.EmailField(source="reservation.professor.email", read_only=True)
    room_code = serializers.CharField(source="reservation.room.code", read_only=True)

    class Meta:
        model = SoftwareRequest
        fields = (
            "id",
            "reservation",
            "machine",
            "name",
            "version",
            "description",
            "status",
            "admin_notes",
            "professor_email",
            "room_code",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "status",
            "admin_notes",
            "professor_email",
            "room_code",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        reservation = attrs.get("reservation") or getattr(self.instance, "reservation", None)
        machine = attrs.get("machine") or getattr(self.instance, "machine", None)
        if machine and reservation and machine.room_id != reservation.room_id:
            raise serializers.ValidationError("A máquina precisa pertencer à sala reservada.")
        return attrs

    def create(self, validated_data):
        instance = SoftwareRequest(**validated_data)
        instance.full_clean()
        instance.save()
        return instance


class SoftwareRequestStatusSerializer(serializers.ModelSerializer):
    """Serializer usado por administradores para alterar o status."""

    class Meta:
        model = SoftwareRequest
        fields = ("status", "admin_notes")

    def validate_status(self, value):
        request_obj: SoftwareRequest = self.instance
        if not request_obj.can_transition(value):
            raise serializers.ValidationError("Transição de status inválida para o estado atual.")
        return value
