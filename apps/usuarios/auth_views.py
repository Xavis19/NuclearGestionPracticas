"""
Vista personalizada de JWT que incluye datos del usuario
"""
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer personalizado que incluye datos del usuario"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Agregar datos del usuario al response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.role,
            'phone': self.user.phone,
        }
        
        # Si es estudiante, agregar datos adicionales
        if self.user.role == 'ESTUDIANTE':
            data['user'].update({
                'matricula': self.user.matricula,
                'carrera': self.user.carrera,
                'semestre': self.user.semestre,
                'promedio': str(self.user.promedio) if self.user.promedio else None,
            })
        
        # Si es profesor, agregar datos adicionales
        if self.user.role == 'PROFESOR':
            data['user'].update({
                'departamento': self.user.departamento,
                'especialidad': self.user.especialidad,
            })
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Vista personalizada de login"""
    serializer_class = CustomTokenObtainPairSerializer
