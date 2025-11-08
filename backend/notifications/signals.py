"""Signals para geração de notificações automáticas."""

from datetime import datetime

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from notifications.models import Notification
from notifications.utils import notify_user
from reservations.models import Reservation
from software_requests.models import SoftwareRequest


@receiver(pre_save, sender=Reservation)
def cache_reservation_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._previous_status = sender.objects.get(pk=instance.pk).status
        except sender.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Reservation)
def notify_reservation(sender, instance, created, **kwargs):
    if created:
        message = (
            f"Sua reserva para a sala {instance.room.name} em {instance.date:%d/%m/%Y}"
            f" das {instance.start_time.strftime('%H:%M')} às {instance.end_time.strftime('%H:%M')} foi confirmada."
        )
        notify_user(
            instance.professor,
            "Reserva confirmada",
            message,
            channels=[Notification.Channel.ALERT, Notification.Channel.EMAIL],
            related_model="Reservation",
            object_id=str(instance.pk),
        )
    else:
        prev = getattr(instance, "_previous_status", None)
        if prev and prev != instance.status and instance.status == Reservation.Status.CANCELLED:
            notify_user(
                instance.professor,
                "Reserva cancelada",
                f"A reserva da sala {instance.room.name} foi cancelada.",
                channels=[Notification.Channel.ALERT, Notification.Channel.EMAIL],
                related_model="Reservation",
                object_id=str(instance.pk),
            )


@receiver(pre_save, sender=SoftwareRequest)
def cache_request_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._previous_status = sender.objects.get(pk=instance.pk).status
        except sender.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=SoftwareRequest)
def notify_software_request(sender, instance, created, **kwargs):
    professor = instance.reservation.professor
    if created:
        notify_user(
            professor,
            "Solicitação registrada",
            f"Recebemos o pedido para {instance.name}.",
            channels=[Notification.Channel.ALERT],
            related_model="SoftwareRequest",
            object_id=str(instance.pk),
        )
    else:
        prev = getattr(instance, "_previous_status", None)
        if prev and prev != instance.status:
            notify_user(
                professor,
                "Status da solicitação atualizado",
                f"O software {instance.name} agora está com status {instance.status}.",
                channels=[Notification.Channel.ALERT, Notification.Channel.EMAIL],
                related_model="SoftwareRequest",
                object_id=str(instance.pk),
            )
