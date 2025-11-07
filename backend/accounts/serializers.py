"""Serializers responsáveis pela autenticação JWT e perfis."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Representa o usuário logado retornando dados públicos."""

    class Meta:
        model = User
        fields = ("id", "email", "matricula", "full_name", "user_type", "photo")
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """Valida e cria novos usuários professores por padrão."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "matricula", "full_name", "user_type", "photo", "password")
        extra_kwargs = {
            "user_type": {"default": User.UserType.PROFESSOR},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Inclui dados do usuário no payload de resposta do login."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_type"] = user.user_type
        token["matricula"] = user.matricula
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data
