"""
Serializers para la app de usuarios.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para User."""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 'first_name', 'last_name',
            'full_name', 'phone', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class EstudianteSerializer(serializers.ModelSerializer):
    """
    Serializer para Estudiantes.
    Incluye campos específicos de estudiante.
    """
    
    full_name = serializers.SerializerMethodField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'full_name', 'phone',
            'matricula', 'carrera', 'semestre', 'promedio',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
        }
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def validate(self, attrs):
        """Validar que las contraseñas coincidan."""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'Las contraseñas no coinciden.'
            })
        return attrs
    
    def validate_email(self, value):
        """Validar que el email sea único."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este email ya está registrado.')
        return value
    
    def validate_username(self, value):
        """Validar que el username sea único."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Este nombre de usuario ya está en uso.')
        return value
    
    def validate_matricula(self, value):
        """Validar que la matrícula sea única si se proporciona."""
        if value and User.objects.filter(matricula=value).exists():
            raise serializers.ValidationError('Esta matrícula ya está registrada.')
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        """Crear estudiante con transacción atómica."""
        # Remover password_confirm
        validated_data.pop('password_confirm', None)
        
        # Extraer password
        password = validated_data.pop('password')
        
        # Establecer rol como ESTUDIANTE
        validated_data['role'] = User.ESTUDIANTE
        
        # Crear usuario
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        return user


class ProfesorSerializer(serializers.ModelSerializer):
    """Serializer para Profesores."""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'phone', 'departamento', 'especialidad',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class CoordinadorSerializer(serializers.ModelSerializer):
    """Serializer para Coordinadores."""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'phone', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar contraseña."""
    
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_old_password(self, value):
        """Validar contraseña actual."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Contraseña actual incorrecta.')
        return value
    
    def validate(self, attrs):
        """Validar que las nuevas contraseñas coincidan."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'Las contraseñas no coinciden.'
            })
        return attrs
    
    def save(self, **kwargs):
        """Cambiar la contraseña."""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
