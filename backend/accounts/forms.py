"""Formulários customizados utilizados no Django Admin."""

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from accounts.models import User


class CustomUserCreationForm(UserCreationForm):
    """Permite criar usuários usando email + matrícula."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "matricula", "user_type")


class CustomUserChangeForm(UserChangeForm):
    """Formulário de edição exibindo campos principais do usuário."""

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("email", "matricula", "user_type", "is_active", "is_staff")
