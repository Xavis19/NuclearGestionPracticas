from django.contrib import admin
from .models import Practica

@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ['id', 'estudiante', 'profesor', 'empresa', 'estado', 'created_at']
    list_filter = ['estado', 'created_at']
    search_fields = ['estudiante__email', 'profesor__email', 'empresa__nombre']
    date_hierarchy = 'created_at'
