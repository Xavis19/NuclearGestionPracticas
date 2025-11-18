from celery import shared_task

@shared_task
def notificar_asignacion_practica(practica_id):
    """Enviar notificación de asignación de práctica."""
    from .models import Practica
    from django.core.mail import send_mail
    
    practica = Practica.objects.get(id=practica_id)
    
    # Enviar email al estudiante
    send_mail(
        subject='Práctica Asignada',
        message=f'Tu práctica ha sido asignada. Profesor: {practica.profesor.get_full_name()}, Empresa: {practica.empresa.nombre}',
        from_email='noreply@practicas.com',
        recipient_list=[practica.estudiante.email],
    )
    
    # Enviar email al profesor
    send_mail(
        subject='Nueva Práctica Asignada',
        message=f'Se te ha asignado una nueva práctica. Estudiante: {practica.estudiante.get_full_name()}',
        from_email='noreply@practicas.com',
        recipient_list=[practica.profesor.email],
    )
