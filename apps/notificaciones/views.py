from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from .models import Notificacion, NotificacionMasiva
from .serializers import NotificacionSerializer, NotificacionMasivaSerializer


class NotificacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Notificaciones.
    - Coordinadora: puede crear y enviar notificaciones a estudiantes
    - Estudiantes: pueden ver sus notificaciones
    - Docentes y Tutores: pueden ver notificaciones (solo lectura)
    """
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar notificaciones según rol."""
        user = self.request.user
        
        if user.is_coordinadora:
            # Coordinadora ve todas
            return Notificacion.objects.all()
        elif user.is_estudiante:
            # Estudiante ve solo sus notificaciones
            return Notificacion.objects.filter(destinatario=user)
        elif user.is_docente_asesor or user.is_tutor_empresarial:
            # Docentes y tutores pueden ver notificaciones de sus estudiantes
            if user.is_docente_asesor:
                estudiantes = user.practicas_asesoradas.values_list('estudiante', flat=True)
            else:
                estudiantes = user.practicas_tutoradas.values_list('estudiante', flat=True)
            return Notificacion.objects.filter(destinatario__in=estudiantes)
        
        return Notificacion.objects.none()
    
    def perform_create(self, serializer):
        """Crear notificación (solo coordinadora)."""
        if not self.request.user.is_coordinadora:
            raise ValidationError('Solo la coordinadora empresarial puede crear notificaciones.')
        
        serializer.save(remitente=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='enviar')
    def enviar(self, request, pk=None):
        """
        Enviar notificación.
        Solo coordinadora.
        """
        if not request.user.is_coordinadora:
            return Response(
                {'error': 'Solo la coordinadora empresarial puede enviar notificaciones.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notificacion = self.get_object()
        
        try:
            notificacion.enviar()
            return Response(
                NotificacionSerializer(notificacion).data,
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='marcar-leida')
    def marcar_leida(self, request, pk=None):
        """
        Marcar notificación como leída.
        Solo el estudiante destinatario.
        """
        notificacion = self.get_object()
        
        if not request.user.is_estudiante or notificacion.destinatario != request.user:
            return Response(
                {'error': 'No tienes permiso para marcar esta notificación.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notificacion.marcar_leida()
        return Response(
            NotificacionSerializer(notificacion).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'], url_path='confirmar')
    def confirmar(self, request, pk=None):
        """
        Confirmar lectura de notificación.
        Solo el estudiante destinatario.
        """
        notificacion = self.get_object()
        
        if not request.user.is_estudiante or notificacion.destinatario != request.user:
            return Response(
                {'error': 'No tienes permiso para confirmar esta notificación.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notificacion.confirmar()
        return Response(
            NotificacionSerializer(notificacion).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='no-leidas')
    def no_leidas(self, request):
        """Obtener notificaciones no leídas del estudiante actual."""
        if not request.user.is_estudiante:
            return Response(
                {'error': 'Solo los estudiantes pueden ver sus notificaciones no leídas.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notificaciones = Notificacion.objects.filter(
            destinatario=request.user,
            estado__in=[Notificacion.PENDIENTE, Notificacion.ENVIADA]
        )
        serializer = self.get_serializer(notificaciones, many=True)
        return Response(serializer.data)


class NotificacionMasivaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Notificaciones Masivas.
    Solo coordinadora puede crear y enviar notificaciones masivas.
    """
    serializer_class = NotificacionMasivaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Solo coordinadora puede ver notificaciones masivas."""
        if self.request.user.is_coordinadora:
            return NotificacionMasiva.objects.all()
        return NotificacionMasiva.objects.none()
    
    def perform_create(self, serializer):
        """Crear notificación masiva (solo coordinadora)."""
        if not self.request.user.is_coordinadora:
            raise ValidationError('Solo la coordinadora empresarial puede crear notificaciones masivas.')
        
        serializer.save(remitente=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='enviar')
    def enviar(self, request, pk=None):
        """
        Enviar notificación masiva.
        Solo coordinadora.
        """
        if not request.user.is_coordinadora:
            return Response(
                {'error': 'Solo la coordinadora empresarial puede enviar notificaciones masivas.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notificacion_masiva = self.get_object()
        
        try:
            notificacion_masiva.enviar()
            return Response(
                NotificacionMasivaSerializer(notificacion_masiva).data,
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
