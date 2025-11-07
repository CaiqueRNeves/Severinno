"""Modelos responsáveis pelas reservas de salas."""

from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from rooms.models import Room

User = settings.AUTH_USER_MODEL


class ReservationQuerySet(models.QuerySet):
    """Consultas auxiliares para reservas."""

    def active(self):
        return self.filter(status=Reservation.Status.SCHEDULED)


class Reservation(models.Model):
    """Reserva feita por um professor para uma sala específica."""

    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Agendada"
        CANCELLED = "CANCELLED", "Cancelada"

    professor = models.ForeignKey(
        User,
        related_name="reservations",
        on_delete=models.CASCADE,
        verbose_name="professor",
    )
    room = models.ForeignKey(
        Room,
        related_name="reservations",
        on_delete=models.CASCADE,
        verbose_name="sala",
    )
    date = models.DateField("data da reserva")
    start_time = models.TimeField("hora de início")
    end_time = models.TimeField("hora de término")
    status = models.CharField(
        "status",
        max_length=15,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    created_at = models.DateTimeField("criada em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizada em", auto_now=True)
    canceled_at = models.DateTimeField("cancelada em", null=True, blank=True)

    objects = ReservationQuerySet.as_manager()

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-date", "-start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["room", "date", "start_time", "end_time"],
                name="unique_room_exact_slot",
                violation_error_message="Já existe uma reserva exata para este horário.",
            )
        ]

    def __str__(self) -> str:
        return f"{self.room.code} - {self.date} {self.start_time}-{self.end_time}"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Hora de início deve ser menor que a hora de término.")

        if self.room_id and self.date and self.start_time and self.end_time:
            if self.overlaps():
                raise ValidationError("Já existe outra reserva para este período.")

        super().clean()

    def overlaps(self):
        """Verifica se há conflitos com outras reservas ativas."""

        return (
            Reservation.objects.active()
            .exclude(pk=self.pk)
            .filter(room=self.room, date=self.date)
            .filter(start_time__lt=self.end_time, end_time__gt=self.start_time)
            .exists()
        )

    def can_cancel(self) -> bool:
        """Permite cancelamento apenas antes do horário agendado."""

        scheduled_start = timezone.make_aware(datetime.combine(self.date, self.start_time))
        return timezone.now() < scheduled_start

    def cancel(self):
        if not self.can_cancel():
            raise ValidationError("A reserva já começou e não pode mais ser cancelada.")
        self.status = Reservation.Status.CANCELLED
        self.canceled_at = timezone.now()
        self.save(update_fields=["status", "canceled_at", "updated_at"])
