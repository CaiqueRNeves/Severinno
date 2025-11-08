"""API dedicada para consulta de logs."""

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from logs.models import AuditLog
from logs.permissions import IsAdminUserType
from logs.serializers import AuditLogSerializer


class AuditLogPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("actor").all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUserType]
    pagination_class = AuditLogPagination
    filterset_fields = ("action", "model", "actor")
    search_fields = ("description",)
