"""Configurações do app core."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Mantém definições principais utilizadas em toda a aplicação."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = "Infraestrutura Core"
