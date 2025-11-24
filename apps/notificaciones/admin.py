from django.contrib import admin
from .models import Notificacion, NotificacionMasiva


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['asunto', 'tipo', 'remitente', 'destinatario', 'estado', 'fecha_envio', 'fecha_lectura']
    list_filter = ['tipo', 'estado', 'enviar_email', 'requiere_confirmacion', 'fecha_envio']
    search_fields = ['asunto', 'mensaje', 'destinatario__email', 'destinatario__first_name']
    readonly_fields = ['fecha_envio', 'fecha_lectura', 'fecha_confirmacion', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('remitente', 'destinatario', 'tipo', 'asunto', 'mensaje')
        }),
        ('Opciones', {
            'fields': ('enviar_email', 'requiere_confirmacion')
        }),
        ('Estado', {
            'fields': ('estado', 'fecha_envio', 'fecha_lectura', 'fecha_confirmacion')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificacionMasiva)
class NotificacionMasivaAdmin(admin.ModelAdmin):
    list_display = ['asunto', 'tipo', 'remitente', 'total_destinatarios', 'enviada', 'fecha_envio']
    list_filter = ['tipo', 'enviada', 'enviar_email', 'requiere_confirmacion', 'fecha_envio']
    search_fields = ['asunto', 'mensaje']
    readonly_fields = ['enviada', 'fecha_envio', 'total_destinatarios', 'created_at', 'updated_at']
    filter_horizontal = ['destinatarios']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('remitente', 'tipo', 'asunto', 'mensaje')
        }),
        ('Destinatarios', {
            'fields': ('destinatarios',)
        }),
        ('Opciones', {
            'fields': ('enviar_email', 'requiere_confirmacion')
        }),
        ('Estado', {
            'fields': ('enviada', 'fecha_envio', 'total_destinatarios')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
