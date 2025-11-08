"""Testes dos endpoints REST do chat."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import Conversation, Message

User = get_user_model()


class ConversationAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin-chat@severinno.com",
            matricula="ADMCHAT",
            password="senha-admin",
            user_type=User.UserType.ADMIN,
        )
        self.professor = User.objects.create_user(
            email="prof-chat@severinno.com",
            matricula="PROFCHAT",
            password="senha-prof",
            user_type=User.UserType.PROFESSOR,
        )
        self.conversation = Conversation.objects.create(title="Suporte Laboratório")
        self.conversation.participants.set([self.admin, self.professor])
        self.list_url = reverse("chat-conversation-list")

    def authenticate(self):
        self.client.force_authenticate(user=self.professor)

    def test_list_conversations(self):
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_message_via_api(self):
        self.authenticate()
        message_url = reverse("chat-message-list")
        payload = {
            "conversation": self.conversation.id,
            "content": "Preciso de suporte no LAB02",
        }
        response = self.client.post(message_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Message.objects.filter(conversation=self.conversation).exists())
