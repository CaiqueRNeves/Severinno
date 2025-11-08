"""Configurações do app de notificações."""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = "Notificações"

    def ready(self):
        from notifications import signals  # noqa: F401
