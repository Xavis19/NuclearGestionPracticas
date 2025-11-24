# Celery tasks para reuniones
from celery import shared_task


@shared_task
def notificar_reunion(reunion_id):
    """Notificar al estudiante sobre una reunión programada."""
    # TODO: Implementar envío de email/notificación
    pass


@shared_task
def notificar_reunion_reprogramada(reunion_id):
    """Notificar al estudiante sobre una reunión reprogramada."""
    # TODO: Implementar envío de email/notificación
    pass


@shared_task
def recordatorio_reuniones_proximas():
    """Tarea periódica para recordar reuniones próximas."""
    # TODO: Implementar recordatorios automáticos
    pass
