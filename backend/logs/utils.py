"""Utilitário central para geração de logs."""

from logs.models import AuditLog


def log_action(actor, action, model, object_id, description, metadata=None):
    AuditLog.objects.create(
        actor=actor,
        action=action,
        model=model,
        object_id=object_id,
        description=description,
        metadata=metadata or {},
    )
