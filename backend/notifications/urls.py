"""Rotas para notificações."""

from rest_framework.routers import SimpleRouter

from notifications.views import NotificationViewSet

router = SimpleRouter()
router.register(r"notifications", NotificationViewSet, basename="notification")

urlpatterns = router.urls
