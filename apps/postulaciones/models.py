from django.db import models
from apps.usuarios.models import User
from apps.vacantes.models import Vacante

class Postulacion(models.Model):
    """RF-002: Postulaciones de estudiantes a vacantes."""
    
    PENDIENTE = 'PENDIENTE'
    SELECCIONADO = 'SELECCIONADO'
    RECHAZADO = 'RECHAZADO'
    
    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (SELECCIONADO, 'Seleccionado'),
        (RECHAZADO, 'Rechazado'),
    ]
    
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postulaciones')
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name='postulaciones')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=PENDIENTE)
    motivacion = models.TextField(verbose_name='Carta de Motivación')
    fecha_seleccion = models.DateTimeField(null=True, blank=True)
    seleccionado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='selecciones_realizadas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Postulación'
        verbose_name_plural = 'Postulaciones'
        unique_together = ['estudiante', 'vacante']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.estudiante.get_full_name()} - {self.vacante.titulo}"
