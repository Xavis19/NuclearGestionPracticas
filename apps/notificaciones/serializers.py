from rest_framework import serializers
from .models import Notificacion, NotificacionMasiva


class NotificacionSerializer(serializers.ModelSerializer):
    """Serializer para Notificaciones."""
    
    remitente_nombre = serializers.CharField(source='remitente.get_full_name', read_only=True)
    destinatario_nombre = serializers.CharField(source='destinatario.get_full_name', read_only=True)
    
    class Meta:
        model = Notificacion
        fields = [
            'id', 'remitente', 'remitente_nombre', 'destinatario', 
            'destinatario_nombre', 'tipo', 'asunto', 'mensaje', 
            'estado', 'fecha_envio', 'fecha_lectura', 'fecha_confirmacion',
            'enviar_email', 'requiere_confirmacion', 'created_at', 'updated_at'
        ]
        read_only_fields = ['estado', 'fecha_envio', 'fecha_lectura', 'fecha_confirmacion', 'created_at', 'updated_at']


class NotificacionMasivaSerializer(serializers.ModelSerializer):
    """Serializer para Notificaciones Masivas."""
    
    remitente_nombre = serializers.CharField(source='remitente.get_full_name', read_only=True)
    
    class Meta:
        model = NotificacionMasiva
        fields = [
            'id', 'remitente', 'remitente_nombre', 'destinatarios',
            'tipo', 'asunto', 'mensaje', 'enviar_email', 
            'requiere_confirmacion', 'enviada', 'fecha_envio',
            'total_destinatarios', 'created_at', 'updated_at'
        ]
        read_only_fields = ['enviada', 'fecha_envio', 'total_destinatarios', 'created_at', 'updated_at']
