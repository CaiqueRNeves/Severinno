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


class ProfessorCreationForm(CustomUserCreationForm):
    """Garante que professores sejam sempre criados com o tipo correto."""

    class Meta(CustomUserCreationForm.Meta):
        model = User
        fields = ("email", "matricula", "full_name", "photo")

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.user_type = User.UserType.PROFESSOR
        user.is_staff = False
        if commit:
            user.save()
        return user


class ProfessorChangeForm(CustomUserChangeForm):
    """Restringe edição para manter professores sempre como tal."""

    user_type = forms.CharField(
        label="Tipo de usuário",
        disabled=True,
        initial=User.UserType.PROFESSOR,
        help_text="Sempre definido como Professor.",
    )

    class Meta(CustomUserChangeForm.Meta):
        model = User
        fields = ("email", "matricula", "full_name", "photo", "is_active")

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.user_type = User.UserType.PROFESSOR
        if commit:
            user.save()
        return user
