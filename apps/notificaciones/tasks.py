# Celery tasks para notificaciones
from celery import shared_task


@shared_task
def enviar_email_notificacion(notificacion_id):
    """Enviar email de notificación al estudiante."""
    # TODO: Implementar envío de email
    pass
