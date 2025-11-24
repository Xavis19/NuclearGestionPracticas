"""
Modelos para la app de entregables.
Sistema para que estudiantes suban entregables y tutores empresariales los evalúen.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.usuarios.models import User
from apps.practicas.models import Practica


class Entregable(models.Model):
    """
    Modelo para los entregables de los estudiantes.
    El estudiante sube documentos/archivos y el tutor empresarial los evalúa.
    """
    
    # Estados
    PENDIENTE = 'PENDIENTE'
    ENVIADO = 'ENVIADO'
    REVISADO = 'REVISADO'
    APROBADO = 'APROBADO'
    RECHAZADO = 'RECHAZADO'
    
    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (ENVIADO, 'Enviado'),
        (REVISADO, 'Revisado'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
    ]
    
    # Relaciones
    practica = models.ForeignKey(
        Practica,
        on_delete=models.CASCADE,
        related_name='entregables',
        verbose_name='Práctica'
    )
    estudiante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='entregables_enviados',
        limit_choices_to={'role': User.ESTUDIANTE},
        verbose_name='Estudiante'
    )
    evaluado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entregables_evaluados',
        limit_choices_to={'role': User.TUTOR_EMPRESARIAL},
        verbose_name='Evaluado por'
    )
    
    # Información del entregable
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    archivo = models.FileField(
        upload_to='entregables/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Archivo'
    )
    
    # Fechas
    fecha_limite = models.DateTimeField(
        verbose_name='Fecha Límite de Entrega'
    )
    fecha_entrega = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=True,
        verbose_name='Fecha de Entrega'
    )
    fecha_evaluacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Evaluación'
    )
    
    # Evaluación (solo tutor empresarial puede evaluar)
    calificacion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Calificación',
        help_text='Calificación del 0 al 100'
    )
    retroalimentacion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Retroalimentación',
        help_text='Comentarios del tutor empresarial'
    )
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=PENDIENTE,
        verbose_name='Estado'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Entregable'
        verbose_name_plural = 'Entregables'
        ordering = ['-fecha_limite', '-created_at']
        indexes = [
            models.Index(fields=['practica', 'estado']),
            models.Index(fields=['estudiante', 'estado']),
            models.Index(fields=['evaluado_por', 'estado']),
            models.Index(fields=['fecha_limite']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.estudiante.get_full_name()}"
    
    def clean(self):
        """Validaciones del modelo."""
        super().clean()
        
        # Validar que el estudiante sea el mismo de la práctica
        if self.estudiante != self.practica.estudiante:
            raise ValidationError({
                'estudiante': 'El estudiante debe ser el mismo de la práctica.'
            })
    
    def enviar(self, archivo):
        """Enviar el entregable."""
        if self.estado not in [self.PENDIENTE, self.RECHAZADO]:
            raise ValidationError('Solo se pueden enviar entregables pendientes o rechazados.')
        
        self.archivo = archivo
        self.estado = self.ENVIADO
        self.save()
    
    def evaluar(self, tutor, calificacion, retroalimentacion='', aprobado=True):
        """
        Evaluar el entregable.
        Solo el tutor empresarial puede evaluar.
        """
        from django.utils import timezone
        
        if self.estado != self.ENVIADO:
            raise ValidationError('Solo se pueden evaluar entregables enviados.')
        
        # Validar que sea el tutor empresarial de la práctica
        if tutor != self.practica.tutor_empresarial:
            raise ValidationError('Solo el tutor empresarial asignado puede evaluar.')
        
        self.evaluado_por = tutor
        self.calificacion = calificacion
        self.retroalimentacion = retroalimentacion
        self.estado = self.APROBADO if aprobado else self.RECHAZADO
        self.fecha_evaluacion = timezone.now()
        self.save()
        
        # TODO: Notificar al estudiante
        # from .tasks import notificar_evaluacion_entregable
        # notificar_evaluacion_entregable.delay(self.id)
    
    @property
    def esta_retrasado(self):
        """Verificar si el entregable está retrasado."""
        from django.utils import timezone
        if self.estado in [self.PENDIENTE, self.ENVIADO]:
            return timezone.now() > self.fecha_limite
        return False
