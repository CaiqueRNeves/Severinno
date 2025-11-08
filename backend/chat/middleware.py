"""Middleware para autenticar WebSockets via JWT (SimpleJWT)."""

from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def _get_user(token: str):
    try:
        access = AccessToken(token)
        return User.objects.get(id=access["user_id"])
    except Exception:  # noqa: BLE001
        return None


class TokenAuthMiddleware:
    """Valida tokens JWT enviados via querystring (?token=)."""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query = parse_qs(scope.get("query_string", b"").decode())
        token = query.get("token", [None])[0]
        scope["user"] = None
        if token:
            user = await _get_user(token)
            if user:
                scope["user"] = user
        return await self.inner(scope, receive, send)


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
