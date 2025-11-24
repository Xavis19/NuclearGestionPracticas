from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from .models import Reunion
from .serializers import (
    ReunionSerializer, MarcarRealizadaSerializer,
    ReprogramarSerializer, CancelarSerializer
)


class ReunionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Reuniones.
    - Docentes Asesores: pueden crear, ver y gestionar reuniones de sus estudiantes
    - Estudiantes: pueden ver sus reuniones
    - Coordinadora: puede ver todas las reuniones
    - Tutores Empresariales: pueden ver reuniones de sus estudiantes
    """
    serializer_class = ReunionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar reuniones según rol."""
        user = self.request.user
        
        if user.is_coordinadora:
            # Coordinadora ve todas
            return Reunion.objects.all()
        elif user.is_docente_asesor:
            # Docente asesor ve sus reuniones
            return Reunion.objects.filter(docente_asesor=user)
        elif user.is_tutor_empresarial:
            # Tutor empresarial ve reuniones de sus estudiantes
            return Reunion.objects.filter(
                practica__tutor_empresarial=user
            )
        elif user.is_estudiante:
            # Estudiante ve solo sus reuniones
            return Reunion.objects.filter(estudiante=user)
        
        return Reunion.objects.none()
    
    def perform_create(self, serializer):
        """Crear reunión (solo docentes asesores)."""
        if not self.request.user.is_docente_asesor:
            raise ValidationError('Solo los docentes asesores pueden crear reuniones.')
        
        reunion = serializer.save(docente_asesor=self.request.user)
        
        # Si es sustentación, actualizar práctica
        if reunion.tipo == Reunion.SUSTENTACION:
            reunion.programar_sustentacion(
                fecha_hora=reunion.fecha_hora,
                lugar=reunion.lugar or '',
                enlace_virtual=reunion.enlace_virtual or '',
                descripcion=reunion.descripcion or ''
            )
        
        # Notificar al estudiante
        reunion.notificar_estudiante()
    
    @action(detail=True, methods=['post'], url_path='marcar-realizada')
    def marcar_realizada(self, request, pk=None):
        """
        Marcar reunión como realizada.
        Solo docentes asesores.
        """
        if not request.user.is_docente_asesor:
            return Response(
                {'error': 'Solo los docentes asesores pueden marcar reuniones como realizadas.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reunion = self.get_object()
        
        # Verificar que sea el docente asesor de la reunión
        if reunion.docente_asesor != request.user:
            return Response(
                {'error': 'No tienes permiso para marcar esta reunión.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MarcarRealizadaSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                reunion.marcar_realizada(
                    notas=serializer.validated_data.get('notas', ''),
                    acuerdos=serializer.validated_data.get('acuerdos', '')
                )
                return Response(
                    ReunionSerializer(reunion).data,
                    status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='reprogramar')
    def reprogramar(self, request, pk=None):
        """
        Reprogramar reunión.
        Solo docentes asesores.
        """
        if not request.user.is_docente_asesor:
            return Response(
                {'error': 'Solo los docentes asesores pueden reprogramar reuniones.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reunion = self.get_object()
        
        # Verificar que sea el docente asesor de la reunión
        if reunion.docente_asesor != request.user:
            return Response(
                {'error': 'No tienes permiso para reprogramar esta reunión.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ReprogramarSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                reunion.reprogramar(
                    nueva_fecha_hora=serializer.validated_data['nueva_fecha_hora']
                )
                return Response(
                    ReunionSerializer(reunion).data,
                    status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        """
        Cancelar reunión.
        Solo docentes asesores.
        """
        if not request.user.is_docente_asesor:
            return Response(
                {'error': 'Solo los docentes asesores pueden cancelar reuniones.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reunion = self.get_object()
        
        # Verificar que sea el docente asesor de la reunión
        if reunion.docente_asesor != request.user:
            return Response(
                {'error': 'No tienes permiso para cancelar esta reunión.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = CancelarSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                reunion.cancelar(
                    motivo=serializer.validated_data.get('motivo', '')
                )
                return Response(
                    ReunionSerializer(reunion).data,
                    status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
