"""Administração dos logs de auditoria."""

from django.contrib import admin

from logs.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "actor", "action", "model", "object_id")
    list_filter = ("action", "model")
    search_fields = ("description", "metadata", "actor__email")
    readonly_fields = ("created_at",)
