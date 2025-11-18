from celery import shared_task

@shared_task
def notificar_seleccion(postulacion_id):
    """Enviar notificación de selección."""
    from .models import Postulacion
    from django.core.mail import send_mail
    
    postulacion = Postulacion.objects.get(id=postulacion_id)
    
    send_mail(
        subject='Has sido seleccionado',
        message=f'Felicidades, has sido seleccionado para la vacante: {postulacion.vacante.titulo}',
        from_email='noreply@practicas.com',
        recipient_list=[postulacion.estudiante.email],
    )
