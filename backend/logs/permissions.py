"""Permissões para consulta de logs."""

from rest_framework.permissions import BasePermission


class IsAdminUserType(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, "user_type", "").upper() == "ADMIN"
