"""Modelos responsáveis pelas notificações do sistema."""

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    class Channel(models.TextChoices):
        ALERT = "ALERT", "Alerta"
        EMAIL = "EMAIL", "Email"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField("título", max_length=140)
    message = models.TextField("mensagem")
    channel = models.CharField("canal", max_length=10, choices=Channel.choices, default=Channel.ALERT)
    is_read = models.BooleanField("já lida", default=False)
    related_model = models.CharField("modelo referenciado", max_length=100, blank=True)
    object_id = models.CharField("ID do objeto", max_length=36, blank=True)
    metadata = models.JSONField("metadados", blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.channel}: {self.title}"
