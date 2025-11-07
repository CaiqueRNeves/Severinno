"""Modelos responsáveis pelos usuários do sistema."""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Gerencia criação de usuários comuns e superusuários."""

    def _create_user(self, email, matricula, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório para criar usuários.")
        if not matricula:
            raise ValueError("A matrícula é obrigatória para criar usuários.")

        email = self.normalize_email(email)
        user = self.model(email=email, matricula=matricula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, matricula, password=None, **extra_fields):
        """Cria um usuário padrão (professor por padrão)."""

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, matricula, password, **extra_fields)

    def create_superuser(self, email, matricula, password=None, **extra_fields):
        """Cria administradores completos para acessar o Django Admin."""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuários precisam ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuários precisam ter is_superuser=True.")

        return self._create_user(email, matricula, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Usuário institucional autenticado via email."""

    class UserType(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        PROFESSOR = "PROFESSOR", "Professor"

    email = models.EmailField("email institucional", unique=True)
    matricula = models.CharField(
        "matrícula",
        max_length=20,
        unique=True,
        validators=[RegexValidator(r"^[A-Za-z0-9_-]+$", "Use apenas letras, números ou _-.")],
    )
    full_name = models.CharField("nome completo", max_length=255, blank=True)
    photo = models.ImageField(
        "foto de perfil",
        upload_to="users/photos/",
        blank=True,
        null=True,
    )
    user_type = models.CharField(
        "tipo de usuário",
        max_length=20,
        choices=UserType.choices,
        default=UserType.PROFESSOR,
    )
    is_active = models.BooleanField("ativo", default=True)
    is_staff = models.BooleanField("staff", default=False)
    date_joined = models.DateTimeField("criado em", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["matricula"]

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["email"]

    def __str__(self) -> str:
        return f"{self.email} ({self.get_user_type_display()})"


class Professor(User):
    """Proxy usado para facilitar a gestão exclusiva de professores no admin."""

    class Meta:
        proxy = True
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ["full_name", "email"]

    def save(self, *args, **kwargs):
        self.user_type = User.UserType.PROFESSOR
        super().save(*args, **kwargs)
