"""Rotas REST do chat."""

from rest_framework.routers import DefaultRouter

from chat.views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"chat/conversations", ConversationViewSet, basename="chat-conversation")
router.register(r"chat/messages", MessageViewSet, basename="chat-message")

urlpatterns = router.urls
