from rest_framework import serializers
from .models import Reunion


class ReunionSerializer(serializers.ModelSerializer):
    """Serializer para Reuniones."""
    
    docente_nombre = serializers.CharField(source='docente_asesor.get_full_name', read_only=True)
    estudiante_nombre = serializers.CharField(source='estudiante.get_full_name', read_only=True)
    es_proxima = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Reunion
        fields = [
            'id', 'practica', 'docente_asesor', 'docente_nombre',
            'estudiante', 'estudiante_nombre', 'tipo', 'titulo',
            'descripcion', 'fecha_hora', 'duracion_minutos', 'lugar',
            'enlace_virtual', 'estado', 'notas_reunion', 'acuerdos',
            'estudiante_notificado', 'fecha_notificacion', 'es_proxima',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['estudiante_notificado', 'fecha_notificacion', 'created_at', 'updated_at']


class MarcarRealizadaSerializer(serializers.Serializer):
    """Serializer para marcar reunión como realizada."""
    notas = serializers.CharField(required=False, allow_blank=True)
    acuerdos = serializers.CharField(required=False, allow_blank=True)


class ReprogramarSerializer(serializers.Serializer):
    """Serializer para reprogramar reunión."""
    nueva_fecha_hora = serializers.DateTimeField(required=True)


class CancelarSerializer(serializers.Serializer):
    """Serializer para cancelar reunión."""
    motivo = serializers.CharField(required=False, allow_blank=True)
