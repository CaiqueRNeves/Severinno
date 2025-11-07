"""Permissões específicas para o domínio de salas e máquinas."""

from rest_framework.permissions import BasePermission


class IsAdminUserType(BasePermission):
    """Permite apenas usuários autenticados com perfil ADMIN."""

    message = "Apenas administradores podem alterar salas e máquinas."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, "user_type", None) == "ADMIN"
