"""Helpers para criação de notificações e disparo de tarefas."""

from notifications.models import Notification
from notifications.tasks import send_email_notification


def notify_user(user, title, message, channels=None, related_model="", object_id="", metadata=None):
    channels = channels or [Notification.Channel.ALERT]
    created = []
    for channel in channels:
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            channel=channel,
            related_model=related_model,
            object_id=object_id,
            metadata=metadata or {},
        )
        created.append(notification)
        if channel == Notification.Channel.EMAIL:
            send_email_notification.delay(title, message, user.email)
    return created
