"""Serializers das notificações."""

from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "title",
            "message",
            "channel",
            "is_read",
            "related_model",
            "object_id",
            "metadata",
            "created_at",
        )
        read_only_fields = fields
