from django.contrib import admin
from .models import Practica

@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ['id', 'estudiante', 'docente_asesor', 'tutor_empresarial', 'empresa', 'estado', 'created_at']
    list_filter = ['estado', 'created_at']
    search_fields = ['estudiante__email', 'docente_asesor__email', 'tutor_empresarial__email', 'empresa__nombre']
    date_hierarchy = 'created_at'
