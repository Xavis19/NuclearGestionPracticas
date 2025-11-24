# Celery tasks para entregables
from celery import shared_task


@shared_task
def notificar_evaluacion_entregable(entregable_id):
    """Notificar al estudiante que su entregable fue evaluado."""
    # TODO: Implementar envío de email/notificación
    pass


@shared_task
def recordatorio_entregables_pendientes():
    """Tarea periódica para recordar entregables pendientes."""
    # TODO: Implementar recordatorios automáticos
    pass
