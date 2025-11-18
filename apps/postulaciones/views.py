from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Postulacion
from .serializers import PostulacionSerializer

class PostulacionViewSet(viewsets.ModelViewSet):
    queryset = Postulacion.objects.all()
    serializer_class = PostulacionSerializer
    
    @action(detail=True, methods=['post'])
    def seleccionar(self, request, pk=None):
        """RF-002: Seleccionar estudiante y enviar notificación."""
        postulacion = self.get_object()
        
        from django.utils import timezone
        postulacion.estado = Postulacion.SELECCIONADO
        postulacion.fecha_seleccion = timezone.now()
        postulacion.seleccionado_por = request.user
        postulacion.save()
        
        # Enviar email vía Celery
        from .tasks import notificar_seleccion
        notificar_seleccion.delay(postulacion.id)
        
        return Response({'message': 'Estudiante seleccionado'}, status=status.HTTP_200_OK)
