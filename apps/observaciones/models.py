# RF-014: Observaciones del Profesor
from django.db import models
from apps.practicas.models import Practica
from apps.usuarios.models import User

class Observacion(models.Model):
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE, related_name='observaciones')
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
