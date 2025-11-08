"""Signals responsáveis por registrar eventos automáticos."""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from accounts.models import User
from logs.utils import log_action
from reservations.models import Reservation
from rooms.models import Machine, Room
from software_requests.models import SoftwareRequest


@receiver(post_save, sender=User)
def log_user_changes(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    log_action(
        actor=instance,
        action=action,
        model="User",
        object_id=str(instance.pk),
        description=f"Usuário {instance.email} {action.lower()}.",
    )


@receiver(post_save, sender=Room)
def log_room_changes(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    log_action(None, action, "Room", str(instance.pk), f"Sala {instance.code} {action.lower()}.")


@receiver(post_save, sender=Machine)
def log_machine_changes(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    log_action(None, action, "Machine", str(instance.pk), f"Máquina {instance.numero_serie} {action.lower()}.")


@receiver(post_delete, sender=Room)
def log_room_delete(sender, instance, **kwargs):
    log_action(None, "DELETED", "Room", str(instance.pk), f"Sala {instance.code} removida.")


@receiver(post_delete, sender=Machine)
def log_machine_delete(sender, instance, **kwargs):
    log_action(None, "DELETED", "Machine", str(instance.pk), f"Máquina {instance.numero_serie} removida.")


@receiver(post_save, sender=Reservation)
def log_reservation(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    log_action(
        actor=instance.professor,
        action=action,
        model="Reservation",
        object_id=str(instance.pk),
        description=f"Reserva da sala {instance.room.code} {action.lower()}.",
        metadata={
            "date": instance.date.isoformat(),
            "start_time": instance.start_time.isoformat(),
            "end_time": instance.end_time.isoformat(),
            "status": instance.status,
        },
    )


@receiver(post_save, sender=SoftwareRequest)
def log_software_request(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    log_action(
        actor=instance.reservation.professor,
        action=action,
        model="SoftwareRequest",
        object_id=str(instance.pk),
        description=f"Solicitação de {instance.name} {action.lower()} com status {instance.status}.",
    )
