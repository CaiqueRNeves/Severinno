"""Tarefas Celery responsáveis por envio de notificações."""

from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_email_notification(subject: str, message: str, recipient: str):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=True)
