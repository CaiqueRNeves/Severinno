"""Middlewares utilitários do app core."""

from django.conf import settings


class ContentSecurityPolicyMiddleware:
    """Adiciona o cabeçalho CSP configurado via settings/env."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        policy = getattr(settings, "CONTENT_SECURITY_POLICY", "")
        if policy:
            response["Content-Security-Policy"] = policy
        return response
