"""
Generador Completo de Aplicaciones
Este script genera TODAS las aplicaciones con modelos, serializers, views, etc.
"""

import os


# Definición completa de aplicaciones
APPS_TEMPLATES = {
    'practicas': {
        '__init__.py': '',
        'apps.py': '''from django.apps import AppConfig

class PracticasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.practicas'
    verbose_name = 'Prácticas'
''',
        'urls.py': '''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PracticaViewSet

router = DefaultRouter()
router.register(r'', PracticaViewSet, basename='practica')

app_name = 'practicas'

urlpatterns = [
    path('', include(router.urls)),
]
''',
        'admin.py': '''from django.contrib import admin
from .models import Practica

@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ['id', 'estudiante', 'profesor', 'empresa', 'estado', 'created_at']
    list_filter = ['estado', 'created_at']
    search_fields = ['estudiante__email', 'profesor__email', 'empresa__nombre']
    date_hierarchy = 'created_at'
''',
        'serializers.py': '''from rest_framework import serializers
from .models import Practica
from apps.usuarios.serializers import UserSerializer, EstudianteSerializer, ProfesorSerializer
from apps.vacantes.serializers import EmpresaSerializer

class PracticaSerializer(serializers.ModelSerializer):
    estudiante_detail = EstudianteSerializer(source='estudiante', read_only=True)
    profesor_detail = ProfesorSerializer(source='profesor', read_only=True)
    empresa_detail = EmpresaSerializer(source='empresa', read_only=True)
    
    class Meta:
        model = Practica
        fields = '__all__'
        read_only_fields = ['asignada_por', 'fecha_asignacion', 'created_at', 'updated_at']
''',
        'views.py': '''from rest_framework import viewsets, status
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
''',
        'tasks.py': '''from celery import shared_task

@shared_task
def notificar_asignacion_practica(practica_id):
    """Enviar notificación de asignación de práctica."""
    from .models import Practica
    from django.core.mail import send_mail
    
    practica = Practica.objects.get(id=practica_id)
    
    # Enviar email al estudiante
    send_mail(
        subject='Práctica Asignada',
        message=f'Tu práctica ha sido asignada. Profesor: {practica.profesor.get_full_name()}, Empresa: {practica.empresa.nombre}',
        from_email='noreply@practicas.com',
        recipient_list=[practica.estudiante.email],
    )
    
    # Enviar email al profesor
    send_mail(
        subject='Nueva Práctica Asignada',
        message=f'Se te ha asignado una nueva práctica. Estudiante: {practica.estudiante.get_full_name()}',
        from_email='noreply@practicas.com',
        recipient_list=[practica.profesor.email],
    )
''',
    },
    
    'postulaciones': {
        '__init__.py': '',
        'apps.py': '''from django.apps import AppConfig

class PostulacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.postulaciones'
    verbose_name = 'Postulaciones'
''',
        'models.py': '''from django.db import models
from apps.usuarios.models import User
from apps.vacantes.models import Vacante

class Postulacion(models.Model):
    """RF-002: Postulaciones de estudiantes a vacantes."""
    
    PENDIENTE = 'PENDIENTE'
    SELECCIONADO = 'SELECCIONADO'
    RECHAZADO = 'RECHAZADO'
    
    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (SELECCIONADO, 'Seleccionado'),
        (RECHAZADO, 'Rechazado'),
    ]
    
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postulaciones')
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE, related_name='postulaciones')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=PENDIENTE)
    motivacion = models.TextField(verbose_name='Carta de Motivación')
    fecha_seleccion = models.DateTimeField(null=True, blank=True)
    seleccionado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='selecciones_realizadas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Postulación'
        verbose_name_plural = 'Postulaciones'
        unique_together = ['estudiante', 'vacante']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.estudiante.get_full_name()} - {self.vacante.titulo}"
''',
        'serializers.py': '''from rest_framework import serializers
from .models import Postulacion

class PostulacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postulacion
        fields = '__all__'
        read_only_fields = ['estudiante', 'estado', 'fecha_seleccion', 'seleccionado_por']
''',
        'views.py': '''from rest_framework import viewsets, status
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
''',
        'tasks.py': '''from celery import shared_task

@shared_task
def notificar_seleccion(postulacion_id):
    """Enviar notificación de selección."""
    from .models import Postulacion
    from django.core.mail import send_mail
    
    postulacion = Postulacion.objects.get(id=postulacion_id)
    
    send_mail(
        subject='Has sido seleccionado',
        message=f'Felicidades, has sido seleccionado para la vacante: {postulacion.vacante.titulo}',
        from_email='noreply@practicas.com',
        recipient_list=[postulacion.estudiante.email],
    )
''',
        'urls.py': '''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostulacionViewSet

router = DefaultRouter()
router.register(r'', PostulacionViewSet, basename='postulacion')

app_name = 'postulaciones'

urlpatterns = [
    path('', include(router.urls)),
]
''',
        'admin.py': '''from django.contrib import admin
from .models import Postulacion

@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'vacante', 'estado', 'created_at']
    list_filter = ['estado', 'created_at']
    search_fields = ['estudiante__email', 'vacante__titulo']
''',
    },
    
    # RESTO DE APPS - Estructura básica
    'documentos': {
        '__init__.py': '',
        'apps.py': '''from django.apps import AppConfig

class DocumentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.documentos'
''',
        'models.py': '''# RF-003: Documentación
from django.db import models

class Documento(models.Model):
    tipo = models.CharField(max_length=100)
    file = models.FileField(upload_to='documentos/')
    hash = models.CharField(max_length=64)
    valido = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
''',
        'urls.py': '''from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
app_name = 'documentos'
urlpatterns = [path('', include(router.urls))]
''',
        'admin.py': '',
        'serializers.py': '',
        'views.py': '',
        'tasks.py': '',
    },
    
    'observaciones': {
        '__init__.py': '',
        'apps.py': '''from django.apps import AppConfig

class ObservacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.observaciones'
''',
        'models.py': '''# RF-014: Observaciones del Profesor
from django.db import models
from apps.practicas.models import Practica
from apps.usuarios.models import User

class Observacion(models.Model):
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE, related_name='observaciones')
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
''',
        'urls.py': '''from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
app_name = 'observaciones'
urlpatterns = [path('', include(router.urls))]
''',
        'admin.py': '',
        'serializers.py': '',
        'views.py': '',
        'tasks.py': '',
    },
}

# Apps con estructura mínima
MINIMAL_APPS = ['contratos', 'tutores', 'encuestas', 'reportes', 'seguimiento', 'evaluaciones', 'cierre']

for app_name in MINIMAL_APPS:
    APPS_TEMPLATES[app_name] = {
        '__init__.py': '',
        'apps.py': f'''from django.apps import AppConfig

class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
''',
        'models.py': f'# TODO: Implementar modelos para {app_name}',
        'urls.py': '''from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
urlpatterns = [path('', include(router.urls))]
''',
        'admin.py': '',
        'serializers.py': '',
        'views.py': '',
        'tasks.py': '',
    }


def create_app(app_name, files):
    """Crear una app con sus archivos."""
    app_path = f'apps/{app_name}'
    os.makedirs(app_path, exist_ok=True)
    
    for filename, content in files.items():
        filepath = os.path.join(app_path, filename)
        with open(filepath, 'w') as f:
            f.write(content)
    
    print(f'✓ App {app_name} creada')


if __name__ == '__main__':
    print('Generando todas las aplicaciones...')
    print('=' * 50)
    
    for app_name, files in APPS_TEMPLATES.items():
        create_app(app_name, files)
    
    print('=' * 50)
    print(f'✓ {len(APPS_TEMPLATES)} aplicaciones generadas correctamente')
    print('\nAplicaciones creadas:')
    for app_name in APPS_TEMPLATES.keys():
        print(f'  - apps.{app_name}')
