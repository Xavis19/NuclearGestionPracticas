"""
Modelos para la app de notificaciones.
Coordinadora empresarial envía notificaciones a estudiantes.
"""

from django.db import models
from django.core.exceptions import ValidationError
from apps.usuarios.models import User


class Notificacion(models.Model):
    """
    Modelo para Notificaciones.
    La coordinadora empresarial envía notificaciones a estudiantes.
    """
    
    # Tipos
    INFORMATIVA = 'INFORMATIVA'
    IMPORTANTE = 'IMPORTANTE'
    URGENTE = 'URGENTE'
    RECORDATORIO = 'RECORDATORIO'
    
    TIPO_CHOICES = [
        (INFORMATIVA, 'Informativa'),
        (IMPORTANTE, 'Importante'),
        (URGENTE, 'Urgente'),
        (RECORDATORIO, 'Recordatorio'),
    ]
    
    # Estados
    PENDIENTE = 'PENDIENTE'
    ENVIADA = 'ENVIADA'
    LEIDA = 'LEIDA'
    
    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (ENVIADA, 'Enviada'),
        (LEIDA, 'Leída'),
    ]
    
    # Relaciones
    remitente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notificaciones_enviadas',
        limit_choices_to={'role': User.COORDINADORA_EMPRESARIAL},
        verbose_name='Remitente'
    )
    destinatario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notificaciones_recibidas',
        limit_choices_to={'role': User.ESTUDIANTE},
        verbose_name='Destinatario',
        help_text='Estudiante que recibirá la notificación'
    )
    
    # Contenido
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default=INFORMATIVA,
        verbose_name='Tipo'
    )
    asunto = models.CharField(
        max_length=200,
        verbose_name='Asunto'
    )
    mensaje = models.TextField(
        verbose_name='Mensaje'
    )
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=PENDIENTE,
        verbose_name='Estado'
    )
    
    # Fechas
    fecha_envio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Envío'
    )
    fecha_lectura = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Lectura'
    )
    
    # Opciones
    enviar_email = models.BooleanField(
        default=True,
        verbose_name='Enviar Email',
        help_text='Enviar también por correo electrónico'
    )
    requiere_confirmacion = models.BooleanField(
        default=False,
        verbose_name='Requiere Confirmación',
        help_text='El estudiante debe confirmar que leyó la notificación'
    )
    fecha_confirmacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Confirmación'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['destinatario', 'estado']),
            models.Index(fields=['remitente', 'fecha_envio']),
            models.Index(fields=['tipo', 'estado']),
        ]
    
    def __str__(self):
        return f"{self.asunto} - {self.destinatario.get_full_name()}"
    
    def enviar(self):
        """Enviar la notificación."""
        from django.utils import timezone
        
        if self.estado != self.PENDIENTE:
            raise ValidationError('Solo se pueden enviar notificaciones pendientes.')
        
        self.estado = self.ENVIADA
        self.fecha_envio = timezone.now()
        self.save()
        
        # Enviar email si está habilitado
        if self.enviar_email:
            # TODO: Implementar envío de email
            # from .tasks import enviar_email_notificacion
            # enviar_email_notificacion.delay(self.id)
            pass
    
    def marcar_leida(self):
        """Marcar notificación como leída."""
        from django.utils import timezone
        
        if self.estado == self.ENVIADA:
            self.estado = self.LEIDA
            self.fecha_lectura = timezone.now()
            self.save()
    
    def confirmar(self):
        """Confirmar que se leyó la notificación."""
        from django.utils import timezone
        
        if self.requiere_confirmacion and self.estado == self.LEIDA:
            self.fecha_confirmacion = timezone.now()
            self.save()


class NotificacionMasiva(models.Model):
    """
    Modelo para envío masivo de notificaciones.
    La coordinadora puede enviar una notificación a múltiples estudiantes a la vez.
    """
    
    # Relaciones
    remitente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notificaciones_masivas_enviadas',
        limit_choices_to={'role': User.COORDINADORA_EMPRESARIAL},
        verbose_name='Remitente'
    )
    destinatarios = models.ManyToManyField(
        User,
        related_name='notificaciones_masivas_recibidas',
        limit_choices_to={'role': User.ESTUDIANTE},
        verbose_name='Destinatarios'
    )
    
    # Contenido
    tipo = models.CharField(
        max_length=20,
        choices=Notificacion.TIPO_CHOICES,
        default=Notificacion.INFORMATIVA,
        verbose_name='Tipo'
    )
    asunto = models.CharField(
        max_length=200,
        verbose_name='Asunto'
    )
    mensaje = models.TextField(
        verbose_name='Mensaje'
    )
    
    # Opciones
    enviar_email = models.BooleanField(
        default=True,
        verbose_name='Enviar Email'
    )
    requiere_confirmacion = models.BooleanField(
        default=False,
        verbose_name='Requiere Confirmación'
    )
    
    # Estado
    enviada = models.BooleanField(
        default=False,
        verbose_name='Enviada'
    )
    fecha_envio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Envío'
    )
    total_destinatarios = models.IntegerField(
        default=0,
        verbose_name='Total de Destinatarios'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Notificación Masiva'
        verbose_name_plural = 'Notificaciones Masivas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.asunto} ({self.total_destinatarios} destinatarios)"
    
    def enviar(self):
        """Enviar la notificación a todos los destinatarios."""
        from django.utils import timezone
        
        if self.enviada:
            raise ValidationError('Esta notificación masiva ya fue enviada.')
        
        destinatarios = self.destinatarios.all()
        self.total_destinatarios = destinatarios.count()
        
        # Crear notificación individual para cada destinatario
        for estudiante in destinatarios:
            notificacion = Notificacion.objects.create(
                remitente=self.remitente,
                destinatario=estudiante,
                tipo=self.tipo,
                asunto=self.asunto,
                mensaje=self.mensaje,
                enviar_email=self.enviar_email,
                requiere_confirmacion=self.requiere_confirmacion
            )
            notificacion.enviar()
        
        self.enviada = True
        self.fecha_envio = timezone.now()
        self.save()
