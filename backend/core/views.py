"""Views do app core."""

from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Endpoint simples para validar o funcionamento básico da API."""

    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request):
        """Retorna informações rápidas de estado para monitoramento."""

        data = {
            "status": "ok",
            "ambiente": "desenvolvimento" if settings.DEBUG else "producao",
            "timestamp": timezone.now().isoformat(),
        }
        return Response(data)
