"""
Views para la app de usuarios.
RF-011: Autenticación y Roles
RF-012: Registro de Estudiantes por Coordinadora
"""

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import User
from .serializers import (
    UserSerializer,
    EstudianteSerializer,
    ProfesorSerializer,
    CoordinadorSerializer,
    ChangePasswordSerializer,
)
from .permissions import IsCoordinador, IsCoordinadorOrProfesor

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para usuarios.
    Solo coordinadores pueden ver la lista completa.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCoordinador]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'matricula']
    ordering_fields = ['created_at', 'email', 'last_name']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener información del usuario actual."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Cambiar contraseña del usuario actual."""
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Contraseña actualizada correctamente.'},
            status=status.HTTP_200_OK
        )


class EstudianteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Estudiantes.
    RF-012: Solo coordinadores pueden crear/editar estudiantes.
    """
    queryset = User.objects.filter(role=User.ESTUDIANTE)
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated, IsCoordinador]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'carrera', 'semestre']
    search_fields = ['email', 'first_name', 'last_name', 'matricula']
    ordering_fields = ['created_at', 'promedio', 'semestre']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Permitir lectura a profesores también.
        """
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsCoordinadorOrProfesor()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """Crear estudiante y enviar email de bienvenida (opcional)."""
        estudiante = serializer.save()
        
        # TODO: Enviar email de bienvenida vía Celery
        # from .tasks import enviar_email_bienvenida
        # enviar_email_bienvenida.delay(estudiante.id)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activar estudiante."""
        estudiante = self.get_object()
        estudiante.is_active = True
        estudiante.save()
        return Response(
            {'message': f'Estudiante {estudiante.get_full_name()} activado.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Desactivar estudiante."""
        estudiante = self.get_object()
        estudiante.is_active = False
        estudiante.save()
        return Response(
            {'message': f'Estudiante {estudiante.get_full_name()} desactivado.'},
            status=status.HTTP_200_OK
        )


class ProfesorViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de Profesores."""
    
    queryset = User.objects.filter(role=User.PROFESOR)
    serializer_class = ProfesorSerializer
    permission_classes = [IsAuthenticated, IsCoordinador]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'departamento']
    search_fields = ['email', 'first_name', 'last_name', 'especialidad']
    ordering_fields = ['created_at', 'last_name']
    ordering = ['last_name']
    
    @action(detail=True, methods=['get'])
    def estudiantes(self, request, pk=None):
        """Obtener estudiantes asignados al profesor."""
        profesor = self.get_object()
        # Esto se implementará cuando tengamos el modelo de Práctica
        from apps.practicas.models import Practica
        practicas = Practica.objects.filter(profesor=profesor)
        estudiantes_ids = practicas.values_list('estudiante_id', flat=True)
        estudiantes = User.objects.filter(id__in=estudiantes_ids)
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)


class CoordinadorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para Coordinadores."""
    
    queryset = User.objects.filter(role=User.COORDINADOR)
    serializer_class = CoordinadorSerializer
    permission_classes = [IsAuthenticated, IsCoordinador]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'last_name']
    ordering = ['last_name']
