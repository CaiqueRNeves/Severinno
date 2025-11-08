"""Testes do consumer WebSocket do chat."""

from asgiref.sync import async_to_sync
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from backend.asgi import application
from chat.models import Conversation

User = get_user_model()


class ChatConsumerTests(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="ws@example.com",
            matricula="WS",
            password="senha",
            user_type=User.UserType.PROFESSOR,
        )
        self.conversation = Conversation.objects.create(title="WS Test")
        self.conversation.participants.add(self.user)

    async def _connect_and_send(self, token):
        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{self.conversation.id}/?token={token}",
        )
        connected, _ = await communicator.connect()
        assert connected
        await communicator.send_json_to({"message": "Olá"})
        response = await communicator.receive_json_from()
        assert response["content"] == "Olá"
        await communicator.disconnect()

    def test_websocket_flow(self):
        token = str(AccessToken.for_user(self.user))
        async_to_sync(self._connect_and_send)(token)
