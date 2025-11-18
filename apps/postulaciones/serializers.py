from rest_framework import serializers
from .models import Postulacion

class PostulacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postulacion
        fields = '__all__'
        read_only_fields = ['estudiante', 'estado', 'fecha_seleccion', 'seleccionado_por']
