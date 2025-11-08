"""Modelos responsáveis pelo histórico de auditoria."""

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class AuditLog(models.Model):
    """Registro genérico que descreve ações relevantes na plataforma."""

    class Action(models.TextChoices):
        CREATED = "CREATED", "Criado"
        UPDATED = "UPDATED", "Atualizado"
        DELETED = "DELETED", "Removido"
        LOGIN = "LOGIN", "Login"
        LOGOUT = "LOGOUT", "Logout"
        CANCELLED = "CANCELLED", "Cancelado"

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="autor",
    )
    action = models.CharField("ação", max_length=20, choices=Action.choices)
    model = models.CharField("modelo afetado", max_length=100)
    object_id = models.CharField("ID do objeto", max_length=36, blank=True)
    description = models.TextField("descrição detalhada")
    metadata = models.JSONField("metadados", blank=True, default=dict)
    created_at = models.DateTimeField("registrado em", auto_now_add=True)

    class Meta:
        verbose_name = "Log de Auditoria"
        verbose_name_plural = "Logs de Auditoria"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.model} ({self.created_at:%Y-%m-%d %H:%M})"
