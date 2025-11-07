"""Configurações administrativas para salas e máquinas."""

from django.contrib import admin

from rooms.models import Machine, Room


class MachineInline(admin.TabularInline):
    """Permite gerenciar máquinas diretamente dentro da sala."""

    model = Machine
    extra = 0
    fields = (
        "hostname",
        "processador",
        "memoria",
        "tipo_memoria",
        "armazenamento",
        "numero_serie",
        "is_available",
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Administração simplificada das salas."""

    list_display = ("code", "name", "location", "capacity", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name", "location")
    inlines = [MachineInline]


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    """Permite visualizar as máquinas com filtros técnicos."""

    list_display = (
        "hostname",
        "room",
        "processador",
        "memoria",
        "tipo_memoria",
        "armazenamento",
        "numero_serie",
        "is_available",
    )
    list_filter = ("tipo_memoria", "is_available", "room")
    search_fields = ("hostname", "numero_serie", "processador", "room__code")
