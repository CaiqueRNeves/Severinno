"""Rotas de acesso aos logs."""

from rest_framework.routers import SimpleRouter

from logs.views import AuditLogViewSet

router = SimpleRouter()
router.register(r"logs", AuditLogViewSet, basename="audit-log")

urlpatterns = router.urls
