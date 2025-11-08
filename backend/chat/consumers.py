"""Consumers ASGI responsáveis pelo chat em tempo real."""

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.models import Conversation, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if user is None or user.is_anonymous:
            await self.close(code=4001)
            return

        self.conversation_id = int(self.scope["url_route"]["kwargs"]["conversation_id"])
        self.group_name = f"chat_{self.conversation_id}"

        if not await self._is_participant(user.id):
            await self.close(code=4003)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        user = self.scope["user"]
        text = content.get("message")
        if not text:
            return
        message = await self._create_message(user.id, text)
        payload = {
            "type": "chat.message",
            "message": {
                "id": message["id"],
                "content": message["content"],
                "sender": message["sender"],
                "created_at": message["created_at"],
            },
        }
        await self.channel_layer.group_send(self.group_name, payload)

    async def chat_message(self, event):
        await self.send_json(event["message"])

    @database_sync_to_async
    def _is_participant(self, user_id: int) -> bool:
        return Conversation.objects.filter(id=self.conversation_id, participants__id=user_id).exists()

    @database_sync_to_async
    def _create_message(self, user_id: int, content: str) -> dict:
        conversation = Conversation.objects.get(id=self.conversation_id)
        message = Message.objects.create(conversation=conversation, sender_id=user_id, content=content)
        return {
            "id": message.id,
            "content": message.content,
            "sender": message.sender.email,
            "created_at": message.created_at.isoformat(),
        }
