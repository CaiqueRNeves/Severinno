"""Modelos responsáveis por solicitações de software vinculadas a reservas."""

from django.core.exceptions import ValidationError
from django.db import models

from reservations.models import Reservation
from rooms.models import Machine


class SoftwareRequest(models.Model):
    """Solicitação feita pelo professor para instalar software em uma máquina reservada."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        APPROVED = "APPROVED", "Aprovada"
        INSTALLED = "INSTALLED", "Instalado"
        REJECTED = "REJECTED", "Rejeitado"
        CANCELLED = "CANCELLED", "Cancelado"

    reservation = models.ForeignKey(
        Reservation,
        related_name="software_requests",
        on_delete=models.CASCADE,
        verbose_name="reserva",
    )
    machine = models.ForeignKey(
        Machine,
        related_name="software_requests",
        on_delete=models.CASCADE,
        verbose_name="máquina",
        null=True,
        blank=True,
    )
    name = models.CharField("nome do software", max_length=120)
    version = models.CharField("versão", max_length=60, blank=True)
    description = models.TextField("detalhes adicionais", blank=True)
    status = models.CharField(
        "status",
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
    )
    admin_notes = models.TextField("anotações administrativas", blank=True)
    created_at = models.DateTimeField("solicitada em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizada em", auto_now=True)

    class Meta:
        verbose_name = "Solicitação de Software"
        verbose_name_plural = "Solicitações de Software"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.version}) - {self.status}"

    def clean(self):
        if self.machine and self.machine.room_id != self.reservation.room_id:
            raise ValidationError("A máquina deve pertencer à mesma sala da reserva.")
        super().clean()

    def can_transition(self, target_status: str) -> bool:
        """Evita mudanças inconsistentes nos fluxos de aprovação."""

        flows = {
            self.Status.PENDING: {self.Status.APPROVED, self.Status.REJECTED, self.Status.CANCELLED},
            self.Status.APPROVED: {self.Status.INSTALLED, self.Status.CANCELLED},
            self.Status.INSTALLED: set(),
            self.Status.REJECTED: set(),
            self.Status.CANCELLED: set(),
        }
        return target_status in flows.get(self.status, set())
