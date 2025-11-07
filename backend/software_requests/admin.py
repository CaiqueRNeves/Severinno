"""Administração das solicitações de software."""

from django.contrib import admin

from software_requests.models import SoftwareRequest


@admin.register(SoftwareRequest)
class SoftwareRequestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "version",
        "reservation",
        "machine",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("name", "reservation__room__name", "reservation__professor__email")
    autocomplete_fields = ("reservation", "machine")
