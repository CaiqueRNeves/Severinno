"""Configurações do app responsável por salas e máquinas."""

from django.apps import AppConfig


class RoomsConfig(AppConfig):
    """Define metadados do app rooms."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rooms'
    verbose_name = "Salas e Máquinas"
