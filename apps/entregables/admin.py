from django.contrib import admin
from .models import Entregable


@admin.register(Entregable)
class EntregableAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'estudiante', 'practica', 'estado', 'calificacion', 'fecha_limite', 'fecha_evaluacion']
    list_filter = ['estado', 'fecha_limite', 'fecha_evaluacion']
    search_fields = ['titulo', 'estudiante__email', 'estudiante__first_name', 'estudiante__last_name']
    readonly_fields = ['created_at', 'updated_at', 'fecha_entrega']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('practica', 'estudiante', 'titulo', 'descripcion')
        }),
        ('Archivo', {
            'fields': ('archivo', 'fecha_limite', 'fecha_entrega')
        }),
        ('Evaluación', {
            'fields': ('estado', 'evaluado_por', 'calificacion', 'retroalimentacion', 'fecha_evaluacion')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
