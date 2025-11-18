# RF-003: Documentación
from django.db import models

class Documento(models.Model):
    tipo = models.CharField(max_length=100)
    file = models.FileField(upload_to='documentos/')
    hash = models.CharField(max_length=64)
    valido = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
