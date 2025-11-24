from django.contrib import admin
from .models import Reunion


@admin.register(Reunion)
class ReunionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'docente_asesor', 'estudiante', 'fecha_hora', 'estado', 'estudiante_notificado']
    list_filter = ['tipo', 'estado', 'fecha_hora', 'estudiante_notificado']
    search_fields = ['titulo', 'estudiante__email', 'docente_asesor__email', 'lugar']
    readonly_fields = ['created_at', 'updated_at', 'fecha_notificacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('practica', 'docente_asesor', 'estudiante', 'tipo', 'titulo', 'descripcion')
        }),
        ('Fecha y Lugar', {
            'fields': ('fecha_hora', 'duracion_minutos', 'lugar', 'enlace_virtual')
        }),
        ('Estado', {
            'fields': ('estado', 'notas_reunion', 'acuerdos')
        }),
        ('Notificaciones', {
            'fields': ('estudiante_notificado', 'fecha_notificacion')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
