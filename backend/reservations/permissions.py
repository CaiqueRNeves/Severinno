"""Permissões especiais para o módulo de reservas."""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProfessorOrAdmin(BasePermission):
    """Apenas professores ou administradores podem acessar o endpoint."""

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, "user_type", "").upper() in {"ADMIN", "PROFESSOR"}


class IsOwnerOrAdmin(BasePermission):
    """Restringe alterações à própria reserva ou administradores."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "user_type", "").upper() == "ADMIN":
            return True
        if request.method in SAFE_METHODS:
            return obj.professor_id == user.id
        return obj.professor_id == user.id
