"""Configuração base do app de contas e autenticação."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Mantém o app focado em usuários e fluxos de autenticação."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = "Gestão de Contas"
