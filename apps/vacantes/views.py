"""
Views para la app de vacantes.
RF-001: Gestión de Vacantes
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models

from .models import Empresa, Vacante
from .serializers import EmpresaSerializer, VacanteSerializer, VacanteListSerializer
from apps.usuarios.permissions import IsCoordinador, IsCoordinadorOrProfesor


class EmpresaViewSet(viewsets.ModelViewSet):
    """ViewSet para Empresas."""
    
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activa', 'verificada', 'sector', 'tamaño']
    search_fields = ['nombre', 'rfc', 'razon_social', 'sector']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']
    
    def get_permissions(self):
        """Solo coordinadores pueden crear/editar."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsCoordinador()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """Guardar quién creó la empresa."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsCoordinador])
    def verificar(self, request, pk=None):
        """Verificar empresa."""
        empresa = self.get_object()
        empresa.verificada = True
        empresa.save()
        return Response({'message': 'Empresa verificada'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def vacantes(self, request, pk=None):
        """Obtener vacantes de la empresa."""
        empresa = self.get_object()
        vacantes = empresa.vacantes.all()
        serializer = VacanteListSerializer(vacantes, many=True)
        return Response(serializer.data)


class VacanteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Vacantes.
    RF-001: Filtros por empresa/estado, búsqueda.
    """
    
    queryset = Vacante.objects.select_related('empresa').all()
    serializer_class = VacanteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'empresa', 'estado', 'modalidad', 'area',
        'semestre_minimo', 'remunerada'
    ]
    search_fields = [
        'titulo', 'descripcion', 'requisitos',
        'empresa__nombre', 'area', 'carreras_solicitadas'
    ]
    ordering_fields = ['created_at', 'fecha_inicio', 'fecha_cierre_convocatoria']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Usar serializer simplificado para listados."""
        if self.action == 'list':
            return VacanteListSerializer
        return VacanteSerializer
    
    def get_permissions(self):
        """Solo coordinadores/empresas pueden crear/editar."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsCoordinador()]
        return super().get_permissions()
    
    def get_queryset(self):
        """Filtrar vacantes según el usuario."""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Estudiantes solo ven vacantes abiertas
        if user.is_estudiante:
            queryset = queryset.filter(estado=Vacante.ABIERTA)
        
        return queryset
    
    def perform_create(self, serializer):
        """Guardar quién creó la vacante."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def verificar_requisitos(self, request, pk=None):
        """Verificar si el estudiante cumple los requisitos."""
        vacante = self.get_object()
        estudiante = request.user
        
        if not estudiante.is_estudiante:
            return Response(
                {'error': 'Solo estudiantes pueden verificar requisitos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        puede, mensaje = vacante.puede_postularse(estudiante)
        
        return Response({
            'puede_postularse': puede,
            'mensaje': mensaje,
            'requisitos': {
                'semestre_minimo': vacante.semestre_minimo,
                'promedio_minimo': vacante.promedio_minimo,
                'carreras_solicitadas': vacante.carreras_solicitadas,
                'estudiante_semestre': estudiante.semestre,
                'estudiante_promedio': estudiante.promedio,
                'estudiante_carrera': estudiante.carrera,
            }
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsCoordinador])
    def cerrar(self, request, pk=None):
        """Cerrar vacante."""
        vacante = self.get_object()
        vacante.estado = Vacante.CERRADA
        vacante.save()
        return Response({'message': 'Vacante cerrada'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsCoordinador])
    def reabrir(self, request, pk=None):
        """Reabrir vacante."""
        vacante = self.get_object()
        if vacante.vacantes_restantes > 0:
            vacante.estado = Vacante.ABIERTA
            vacante.save()
            return Response({'message': 'Vacante reabierta'}, status=status.HTTP_200_OK)
        return Response(
            {'error': 'No hay vacantes disponibles'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def disponibles(self, request):
        """Obtener solo vacantes disponibles para postulación."""
        vacantes = self.get_queryset().filter(
            estado=Vacante.ABIERTA
        ).exclude(
            vacantes_ocupadas__gte=models.F('vacantes_disponibles')
        )
        
        serializer = VacanteListSerializer(vacantes, many=True)
        return Response(serializer.data)
