"""Configurações personalizadas do Django Admin para usuários."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Ajusta a interface administrativa às regras do modelo customizado."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    ordering = ("email",)
    list_display = ("email", "matricula", "user_type", "is_staff", "is_active")
    list_filter = ("user_type", "is_staff", "is_active")
    search_fields = ("email", "matricula", "full_name")

    fieldsets = (
        (_("Credenciais"), {"fields": ("email", "password", "matricula")}),
        (_("Perfil"), {"fields": ("full_name", "user_type", "photo")}),
        (
            _("Permissões"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Datas importantes"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            _("Novo usuário"),
            {
                "classes": ("wide",),
                "fields": ("email", "matricula", "user_type", "password1", "password2"),
            },
        ),
    )
