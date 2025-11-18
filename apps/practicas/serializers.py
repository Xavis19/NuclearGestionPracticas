from rest_framework import serializers
from .models import Practica
from apps.usuarios.serializers import UserSerializer, EstudianteSerializer, ProfesorSerializer
from apps.vacantes.serializers import EmpresaSerializer

class PracticaSerializer(serializers.ModelSerializer):
    estudiante_detail = EstudianteSerializer(source='estudiante', read_only=True)
    profesor_detail = ProfesorSerializer(source='profesor', read_only=True)
    empresa_detail = EmpresaSerializer(source='empresa', read_only=True)
    
    class Meta:
        model = Practica
        fields = '__all__'
        read_only_fields = ['asignada_por', 'fecha_asignacion', 'created_at', 'updated_at']
