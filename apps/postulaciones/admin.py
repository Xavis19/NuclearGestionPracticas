from django.contrib import admin
from .models import Postulacion

@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'vacante', 'estado', 'created_at']
    list_filter = ['estado', 'created_at']
    search_fields = ['estudiante__email', 'vacante__titulo']
