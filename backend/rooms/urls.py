"""Rotas referentes às salas e máquinas."""

from rest_framework.routers import DefaultRouter

from rooms.views import MachineViewSet, RoomViewSet

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"machines", MachineViewSet, basename="machine")

urlpatterns = router.urls
