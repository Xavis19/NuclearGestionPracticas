"""
Serializers para la app de vacantes.
"""

from rest_framework import serializers
from .models import Empresa, Vacante


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para Empresa."""
    
    class Meta:
        model = Empresa
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class VacanteSerializer(serializers.ModelSerializer):
    """Serializer para Vacante."""
    
    empresa_detail = EmpresaSerializer(source='empresa', read_only=True)
    vacantes_restantes = serializers.ReadOnlyField()
    esta_abierta = serializers.ReadOnlyField()
    
    class Meta:
        model = Vacante
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'vacantes_ocupadas']
    
    def validate(self, attrs):
        """Validaciones adicionales."""
        if attrs.get('fecha_cierre_convocatoria') and attrs.get('fecha_inicio'):
            if attrs['fecha_cierre_convocatoria'] >= attrs['fecha_inicio']:
                raise serializers.ValidationError({
                    'fecha_cierre_convocatoria': 'Debe ser anterior a la fecha de inicio.'
                })
        return attrs


class VacanteListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de vacantes."""
    
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    vacantes_restantes = serializers.ReadOnlyField()
    
    class Meta:
        model = Vacante
        fields = [
            'id', 'titulo', 'empresa_nombre', 'area', 'modalidad',
            'ubicacion', 'vacantes_disponibles', 'vacantes_restantes',
            'estado', 'fecha_inicio', 'fecha_cierre_convocatoria', 'created_at'
        ]
