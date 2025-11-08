"""Serializers para conversas e mensagens."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from chat.models import Conversation, Message

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source="sender.email", read_only=True)

    class Meta:
        model = Message
        fields = ("id", "conversation", "sender", "sender_email", "content", "created_at")
        read_only_fields = ("sender", "sender_email", "created_at", "conversation")


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "title", "participants", "created_at", "last_message")

    def get_last_message(self, obj):
        message = obj.messages.order_by("-created_at").first()
        if not message:
            return None
        return MessageSerializer(message).data
