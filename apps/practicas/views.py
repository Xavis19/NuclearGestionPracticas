from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Practica
from .serializers import PracticaSerializer
from apps.usuarios.permissions import IsCoordinador, IsCoordinadorOrProfesor

class PracticaViewSet(viewsets.ModelViewSet):
    queryset = Practica.objects.all()
    serializer_class = PracticaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'estudiante', 'profesor', 'empresa']
    search_fields = ['estudiante__email', 'profesor__email', 'empresa__nombre']
    ordering_fields = ['created_at', 'fecha_inicio']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'asignar']:
            return [IsAuthenticated(), IsCoordinador()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsCoordinador])
    def asignar(self, request, pk=None):
        """RF-013: Asignar profesor y empresa a la práctica."""
        practica = self.get_object()
        profesor_id = request.data.get('profesor_id')
        empresa_id = request.data.get('empresa_id')
        
        from apps.usuarios.models import User
        from apps.vacantes.models import Empresa
        
        try:
            profesor = User.objects.get(id=profesor_id, role=User.PROFESOR)
            empresa = Empresa.objects.get(id=empresa_id)
            
            practica.asignar(profesor, empresa, request.user)
            
            return Response({
                'message': 'Práctica asignada exitosamente',
                'practica': self.get_serializer(practica).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
