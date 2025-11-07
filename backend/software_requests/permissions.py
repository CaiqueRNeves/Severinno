"""Permissões específicas para solicitações de software."""

from rest_framework.permissions import BasePermission


class IsAdminOrOwnerReservation(BasePermission):
    """Permite que admins gerenciem tudo e professores apenas suas reservas."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "user_type", "").upper() == "ADMIN":
            return True
        return obj.reservation.professor_id == user.id

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, "user_type", "").upper() in {"ADMIN", "PROFESSOR"}
