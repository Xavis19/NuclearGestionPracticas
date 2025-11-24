"""
Modelos para la app de reuniones.
Docentes asesores programan reuniones semanales de seguimiento y la sustentación final.
"""

from django.db import models
from django.core.exceptions import ValidationError
from apps.usuarios.models import User
from apps.practicas.models import Practica


class Reunion(models.Model):
    """
    Modelo para Reuniones de Seguimiento.
    El docente asesor programa reuniones semanales con el estudiante.
    """
    
    # Tipos
    SEGUIMIENTO = 'SEGUIMIENTO'
    SUSTENTACION = 'SUSTENTACION'
    
    TIPO_CHOICES = [
        (SEGUIMIENTO, 'Reunión de Seguimiento'),
        (SUSTENTACION, 'Sustentación'),
    ]
    
    # Estados
    PROGRAMADA = 'PROGRAMADA'
    REALIZADA = 'REALIZADA'
    CANCELADA = 'CANCELADA'
    REPROGRAMADA = 'REPROGRAMADA'
    
    ESTADO_CHOICES = [
        (PROGRAMADA, 'Programada'),
        (REALIZADA, 'Realizada'),
        (CANCELADA, 'Cancelada'),
        (REPROGRAMADA, 'Reprogramada'),
    ]
    
    # Relaciones
    practica = models.ForeignKey(
        Practica,
        on_delete=models.CASCADE,
        related_name='reuniones',
        verbose_name='Práctica'
    )
    docente_asesor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reuniones_programadas',
        limit_choices_to={'role': User.DOCENTE_ASESOR},
        verbose_name='Docente Asesor'
    )
    estudiante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reuniones_asignadas',
        limit_choices_to={'role': User.ESTUDIANTE},
        verbose_name='Estudiante'
    )
    
    # Información de la reunión
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default=SEGUIMIENTO,
        verbose_name='Tipo'
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    
    # Fecha y hora
    fecha_hora = models.DateTimeField(
        verbose_name='Fecha y Hora'
    )
    duracion_minutos = models.IntegerField(
        default=60,
        verbose_name='Duración (minutos)'
    )
    
    # Ubicación
    lugar = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Lugar'
    )
    enlace_virtual = models.URLField(
        blank=True,
        null=True,
        verbose_name='Enlace Virtual',
        help_text='Enlace de videollamada (Zoom, Meet, Teams, etc.)'
    )
    
    # Estado y notas
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=PROGRAMADA,
        verbose_name='Estado'
    )
    notas_reunion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas de la Reunión',
        help_text='Notas tomadas durante o después de la reunión'
    )
    acuerdos = models.TextField(
        blank=True,
        null=True,
        verbose_name='Acuerdos',
        help_text='Acuerdos y compromisos tomados'
    )
    
    # Notificaciones
    estudiante_notificado = models.BooleanField(
        default=False,
        verbose_name='Estudiante Notificado'
    )
    fecha_notificacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Notificación'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Reunión'
        verbose_name_plural = 'Reuniones'
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['practica', 'estado']),
            models.Index(fields=['docente_asesor', 'fecha_hora']),
            models.Index(fields=['estudiante', 'fecha_hora']),
            models.Index(fields=['tipo', 'estado']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.estudiante.get_full_name()} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"
    
    def clean(self):
        """Validaciones del modelo."""
        super().clean()
        
        # Validar que el docente asesor sea el mismo de la práctica
        if self.docente_asesor != self.practica.docente_asesor:
            raise ValidationError({
                'docente_asesor': 'El docente asesor debe ser el mismo de la práctica.'
            })
        
        # Validar que el estudiante sea el mismo de la práctica
        if self.estudiante != self.practica.estudiante:
            raise ValidationError({
                'estudiante': 'El estudiante debe ser el mismo de la práctica.'
            })
        
        # Solo puede haber una sustentación por práctica
        if self.tipo == self.SUSTENTACION:
            sustentaciones = Reunion.objects.filter(
                practica=self.practica,
                tipo=self.SUSTENTACION
            ).exclude(pk=self.pk)
            
            if sustentaciones.exists():
                raise ValidationError('Ya existe una sustentación programada para esta práctica.')
    
    def programar_sustentacion(self, fecha_hora, lugar, enlace_virtual='', descripcion=''):
        """
        Actualizar información de sustentación en la práctica.
        """
        if self.tipo == self.SUSTENTACION:
            self.practica.fecha_sustentacion = fecha_hora
            self.practica.lugar_sustentacion = lugar
            self.practica.observaciones_sustentacion = descripcion
            self.practica.save()
    
    def marcar_realizada(self, notas='', acuerdos=''):
        """Marcar reunión como realizada."""
        if self.estado != self.PROGRAMADA:
            raise ValidationError('Solo se pueden marcar como realizadas reuniones programadas.')
        
        self.estado = self.REALIZADA
        self.notas_reunion = notas
        self.acuerdos = acuerdos
        self.save()
    
    def cancelar(self, motivo=''):
        """Cancelar reunión."""
        if self.estado == self.REALIZADA:
            raise ValidationError('No se pueden cancelar reuniones ya realizadas.')
        
        self.estado = self.CANCELADA
        if motivo:
            self.notas_reunion = f"Cancelada: {motivo}"
        self.save()
    
    def reprogramar(self, nueva_fecha_hora):
        """Reprogramar reunión."""
        from django.utils import timezone
        
        if self.estado == self.REALIZADA:
            raise ValidationError('No se pueden reprogramar reuniones ya realizadas.')
        
        self.fecha_hora = nueva_fecha_hora
        self.estado = self.REPROGRAMADA
        self.estudiante_notificado = False
        self.save()
        
        # TODO: Notificar reprogramación
        # from .tasks import notificar_reunion_reprogramada
        # notificar_reunion_reprogramada.delay(self.id)
    
    def notificar_estudiante(self):
        """Notificar al estudiante sobre la reunión."""
        from django.utils import timezone
        
        if not self.estudiante_notificado:
            # TODO: Enviar email/notificación
            # from .tasks import notificar_reunion
            # notificar_reunion.delay(self.id)
            
            self.estudiante_notificado = True
            self.fecha_notificacion = timezone.now()
            self.save()
    
    @property
    def es_proxima(self):
        """Verificar si la reunión es próxima (en las próximas 24 horas)."""
        from django.utils import timezone
        from datetime import timedelta
        
        if self.estado == self.PROGRAMADA:
            ahora = timezone.now()
            return ahora <= self.fecha_hora <= ahora + timedelta(days=1)
        return False
