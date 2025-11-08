"""Serializers para leitura de logs."""

from rest_framework import serializers

from logs.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    actor_email = serializers.EmailField(source="actor.email", read_only=True)

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "actor",
            "actor_email",
            "action",
            "model",
            "object_id",
            "description",
            "metadata",
            "created_at",
        )
        read_only_fields = fields
