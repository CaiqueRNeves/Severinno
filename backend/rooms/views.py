"""ViewSets para gerenciamento de salas e máquinas."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rooms.models import Machine, Room
from rooms.permissions import IsAdminUserType
from rooms.serializers import MachineSerializer, RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """CRUD completo de salas disponível apenas para administradores."""

    queryset = Room.objects.all().order_by("name")
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdminUserType]


class MachineViewSet(viewsets.ModelViewSet):
    """CRUD completo de máquinas ligado às salas."""

    queryset = Machine.objects.select_related("room").all()
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticated, IsAdminUserType]
