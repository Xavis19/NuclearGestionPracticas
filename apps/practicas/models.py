"""
Modelos para la app de prácticas.
RF-013: Asignación de Profesor y Empresa
"""

from django.db import models
from django.core.exceptions import ValidationError
from apps.usuarios.models import User
from apps.vacantes.models import Empresa


class Practica(models.Model):
    """
    Modelo para Prácticas Profesionales.
    RF-013: Asignación de profesor y empresa por coordinadora.
    """
    
    # Estados
    PENDIENTE = 'PENDIENTE'
    ASIGNADA = 'ASIGNADA'
    EN_CURSO = 'EN_CURSO'
    COMPLETADA = 'COMPLETADA'
    CANCELADA = 'CANCELADA'
    
    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (ASIGNADA, 'Asignada'),
        (EN_CURSO, 'En Curso'),
        (COMPLETADA, 'Completada'),
        (CANCELADA, 'Cancelada'),
    ]
    
    # Relaciones principales
    estudiante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='practicas',
        limit_choices_to={'role': User.ESTUDIANTE},
        verbose_name='Estudiante'
    )
    profesor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='practicas_supervisadas',
        limit_choices_to={'role': User.PROFESOR},
        verbose_name='Profesor Asignado'
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='practicas',
        verbose_name='Empresa'
    )
    
    # Información de la práctica
    area_practica = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Área de Práctica'
    )
    proyecto = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción del Proyecto'
    )
    
    # Fechas
    fecha_inicio = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Inicio'
    )
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Fin'
    )
    fecha_asignacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Asignación'
    )
    
    # Estado y seguimiento
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=PENDIENTE,
        verbose_name='Estado'
    )
    cerrada = models.BooleanField(
        default=False,
        verbose_name='Cerrada'
    )
    
    # Calificación final
    calificacion_final = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Calificación Final'
    )
    
    # Metadata
    asignada_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='practicas_asignadas',
        limit_choices_to={'role': User.COORDINADOR},
        verbose_name='Asignada por'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    class Meta:
        verbose_name = 'Práctica'
        verbose_name_plural = 'Prácticas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['estudiante', 'estado']),
            models.Index(fields=['profesor', 'estado']),
            models.Index(fields=['empresa', 'estado']),
            models.Index(fields=['estado', 'created_at']),
        ]
        constraints = [
            # Un estudiante no puede tener múltiples prácticas activas
            models.UniqueConstraint(
                fields=['estudiante'],
                condition=models.Q(estado__in=['ASIGNADA', 'EN_CURSO']),
                name='unique_active_practica_per_estudiante'
            )
        ]
    
    def __str__(self):
        return f"Práctica de {self.estudiante.get_full_name()} - {self.get_estado_display()}"
    
    def clean(self):
        """Validaciones del modelo."""
        super().clean()
        
        # Validar que empresa esté activa
        if self.empresa and not self.empresa.activa:
            raise ValidationError({
                'empresa': 'La empresa debe estar activa.'
            })
        
        # Validar fechas
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin <= self.fecha_inicio:
                raise ValidationError({
                    'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'
                })
    
    def asignar(self, profesor, empresa, asignada_por):
        """
        Asignar profesor y empresa a la práctica.
        RF-013: Solo coordinadora puede asignar.
        """
        from django.conf import settings
        from django.utils import timezone
        
        # Validar que empresa esté activa
        if not empresa.activa:
            raise ValidationError('La empresa debe estar activa.')
        
        # Validar cupo del profesor
        practicas_activas = Practica.objects.filter(
            profesor=profesor,
            estado__in=[self.ASIGNADA, self.EN_CURSO]
        ).count()
        
        max_estudiantes = getattr(settings, 'MAX_ESTUDIANTES_POR_PROFESOR', 10)
        
        if practicas_activas >= max_estudiantes:
            raise ValidationError(
                f'El profesor ya tiene el máximo de {max_estudiantes} estudiantes asignados.'
            )
        
        # Asignar
        self.profesor = profesor
        self.empresa = empresa
        self.asignada_por = asignada_por
        self.estado = self.ASIGNADA
        self.fecha_asignacion = timezone.now()
        self.save()
        
        # TODO: Enviar notificación por email vía Celery
        # from .tasks import notificar_asignacion_practica
        # notificar_asignacion_practica.delay(self.id)
        
        return self
    
    def iniciar(self):
        """Iniciar la práctica."""
        if self.estado != self.ASIGNADA:
            raise ValidationError('La práctica debe estar en estado ASIGNADA.')
        
        self.estado = self.EN_CURSO
        self.save()
    
    def completar(self, calificacion=None):
        """Completar la práctica."""
        if self.estado != self.EN_CURSO:
            raise ValidationError('La práctica debe estar en curso.')
        
        self.estado = self.COMPLETADA
        if calificacion:
            self.calificacion_final = calificacion
        self.save()
    
    def cancelar(self):
        """Cancelar la práctica."""
        self.estado = self.CANCELADA
        self.save()
