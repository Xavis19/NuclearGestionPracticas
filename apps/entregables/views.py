from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from .models import Entregable
from .serializers import EntregableSerializer, EvaluarEntregableSerializer
from apps.usuarios.models import User


class EntregableViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Entregables.
    - Estudiantes: pueden ver sus entregables y subirlos
    - Tutores Empresariales: pueden ver y evaluar entregables de sus estudiantes
    - Docentes Asesores: pueden ver entregables de sus estudiantes
    - Coordinadora: puede ver todos los entregables
    """
    serializer_class = EntregableSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar entregables según rol."""
        user = self.request.user
        
        if user.is_coordinadora:
            # Coordinadora ve todos
            return Entregable.objects.all()
        elif user.is_docente_asesor:
            # Docente asesor ve entregables de sus estudiantes
            return Entregable.objects.filter(
                practica__docente_asesor=user
            )
        elif user.is_tutor_empresarial:
            # Tutor empresarial ve entregables de sus estudiantes
            return Entregable.objects.filter(
                practica__tutor_empresarial=user
            )
        elif user.is_estudiante:
            # Estudiante ve solo sus entregables
            return Entregable.objects.filter(estudiante=user)
        
        return Entregable.objects.none()
    
    def perform_create(self, serializer):
        """Crear entregable (solo estudiantes)."""
        if not self.request.user.is_estudiante:
            raise ValidationError('Solo los estudiantes pueden crear entregables.')
        
        serializer.save(estudiante=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='evaluar')
    def evaluar(self, request, pk=None):
        """
        Evaluar un entregable.
        Solo tutores empresariales pueden evaluar.
        """
        if not request.user.is_tutor_empresarial:
            return Response(
                {'error': 'Solo los tutores empresariales pueden evaluar entregables.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        entregable = self.get_object()
        serializer = EvaluarEntregableSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                entregable.evaluar(
                    tutor=request.user,
                    calificacion=serializer.validated_data['calificacion'],
                    retroalimentacion=serializer.validated_data.get('retroalimentacion', ''),
                    aprobado=serializer.validated_data.get('aprobado', True)
                )
                return Response(
                    EntregableSerializer(entregable).data,
                    status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='enviar')
    def enviar(self, request, pk=None):
        """
        Enviar un entregable.
        Solo estudiantes pueden enviar.
        """
        if not request.user.is_estudiante:
            return Response(
                {'error': 'Solo los estudiantes pueden enviar entregables.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        entregable = self.get_object()
        
        # Verificar que el estudiante sea el dueño
        if entregable.estudiante != request.user:
            return Response(
                {'error': 'No tienes permiso para enviar este entregable.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response(
                {'error': 'Debe proporcionar un archivo.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            entregable.enviar(archivo)
            return Response(
                EntregableSerializer(entregable).data,
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
