from rest_framework import serializers
from .models import Entregable
from apps.usuarios.models import User


class EntregableSerializer(serializers.ModelSerializer):
    """Serializer para Entregables."""
    
    estudiante_nombre = serializers.CharField(source='estudiante.get_full_name', read_only=True)
    evaluador_nombre = serializers.CharField(source='evaluado_por.get_full_name', read_only=True)
    esta_retrasado = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Entregable
        fields = [
            'id', 'practica', 'estudiante', 'estudiante_nombre',
            'titulo', 'descripcion', 'archivo', 'fecha_limite',
            'fecha_entrega', 'fecha_evaluacion', 'estado',
            'calificacion', 'retroalimentacion', 'evaluado_por',
            'evaluador_nombre', 'esta_retrasado', 'created_at', 'updated_at'
        ]
        read_only_fields = ['fecha_entrega', 'fecha_evaluacion', 'estado', 'created_at', 'updated_at']


class EvaluarEntregableSerializer(serializers.Serializer):
    """Serializer para evaluar un entregable."""
    
    calificacion = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=True
    )
    retroalimentacion = serializers.CharField(required=False, allow_blank=True)
    aprobado = serializers.BooleanField(default=True)
