"""Configurações personalizadas do Django Admin para usuários."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from accounts.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    ProfessorChangeForm,
    ProfessorCreationForm,
)
from accounts.models import Professor, User


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


@admin.register(Professor)
class ProfessorAdmin(BaseUserAdmin):
    """Interface dedicada ao CRUD de professores (proxy do usuário)."""

    add_form = ProfessorCreationForm
    form = ProfessorChangeForm
    model = Professor
    list_display = ("full_name", "email", "matricula", "photo_thumb", "is_active")
    list_filter = ("is_active",)
    search_fields = ("email", "matricula", "full_name")
    ordering = ("full_name",)
    readonly_fields = ("photo_preview",)

    fieldsets = (
        (_("Identificação"), {"fields": ("email", "matricula", "full_name")}),
        (_("Foto"), {"fields": ("photo", "photo_preview")}),
        (_("Status"), {"fields": ("is_active",)}),
    )
    add_fieldsets = (
        (
            _("Novo professor"),
            {
                "classes": ("wide",),
                "fields": ("email", "matricula", "full_name", "photo", "password1", "password2"),
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(user_type=User.UserType.PROFESSOR)

    def save_model(self, request, obj, form, change):
        obj.user_type = User.UserType.PROFESSOR
        super().save_model(request, obj, form, change)

    @staticmethod
    def photo_thumb(obj):
        if obj.photo:
            return format_html(
                '<img src="{}" alt="Foto" width="48" height="48" style="border-radius:50%; object-fit:cover;">',
                obj.photo.url,
            )
        return "—"

    @staticmethod
    def photo_preview(obj):
        if obj.photo:
            return format_html(
                '<img src="{}" alt="Foto do professor" style="max-width:200px;border-radius:8px;">',
                obj.photo.url,
            )
        return "Nenhuma foto enviada."

    photo_thumb.short_description = "Foto"
    photo_preview.short_description = "Pré-visualização"


admin.site.site_header = "Severinno • Painel Administrativo"
admin.site.site_title = "Severinno Admin"
admin.site.index_title = "Bem-vindo ao painel Severinno"
