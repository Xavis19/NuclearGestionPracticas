"""
Admin para la app de vacantes.
"""

from django.contrib import admin
from .models import Empresa, Vacante


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    """Admin para Empresa."""
    
    list_display = [
        'nombre', 'rfc', 'sector', 'tamaño',
        'activa', 'verificada', 'created_at'
    ]
    list_filter = ['activa', 'verificada', 'sector', 'tamaño', 'created_at']
    search_fields = ['nombre', 'rfc', 'razon_social', 'email']
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'rfc', 'razon_social', 'sector', 'tamaño')
        }),
        ('Contacto', {
            'fields': (
                'direccion', 'telefono', 'email', 'sitio_web',
                'contacto_nombre', 'contacto_puesto',
                'contacto_email', 'contacto_telefono'
            )
        }),
        ('Estado', {
            'fields': ('activa', 'verificada')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Vacante)
class VacanteAdmin(admin.ModelAdmin):
    """Admin para Vacante."""
    
    list_display = [
        'titulo', 'empresa', 'area', 'modalidad', 'estado',
        'vacantes_disponibles', 'vacantes_ocupadas',
        'fecha_inicio', 'created_at'
    ]
    list_filter = [
        'estado', 'modalidad', 'remunerada',
        'empresa', 'created_at', 'fecha_inicio'
    ]
    search_fields = [
        'titulo', 'descripcion', 'requisitos',
        'empresa__nombre', 'area', 'carreras_solicitadas'
    ]
    readonly_fields = ['created_by', 'created_at', 'updated_at', 'vacantes_restantes']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('empresa', 'titulo', 'descripcion', 'area')
        }),
        ('Requisitos', {
            'fields': (
                'requisitos', 'carreras_solicitadas',
                'semestre_minimo', 'promedio_minimo'
            )
        }),
        ('Detalles', {
            'fields': (
                'modalidad', 'ubicacion', 'horario', 'duracion_meses'
            )
        }),
        ('Cupos y Fechas', {
            'fields': (
                'vacantes_disponibles', 'vacantes_ocupadas',
                'fecha_inicio', 'fecha_cierre_convocatoria'
            )
        }),
        ('Beneficios', {
            'fields': (
                'remunerada', 'monto_apoyo', 'beneficios_adicionales'
            ),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def vacantes_restantes(self, obj):
        return obj.vacantes_restantes
    vacantes_restantes.short_description = 'Vacantes Restantes'
