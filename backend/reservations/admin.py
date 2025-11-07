"""Administração de reservas."""

from django.contrib import admin

from reservations.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "professor",
        "date",
        "start_time",
        "end_time",
        "status",
    )
    list_filter = ("status", "date", "room")
    search_fields = ("room__name", "room__code", "professor__email")
    readonly_fields = ("created_at", "updated_at", "canceled_at")
