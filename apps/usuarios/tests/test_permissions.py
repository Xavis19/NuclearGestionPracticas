"""
Pruebas para permisos personalizados.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from apps.usuarios.permissions import IsCoordinador, IsCoordinadorOrProfesor

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestIsCoordinadorPermission:
    """Pruebas para el permiso IsCoordinador."""
    
    def test_coordinador_has_permission(self, coordinador_factory):
        """Coordinador debe tener permiso."""
        coordinador = coordinador_factory()
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = coordinador
        
        permission = IsCoordinador()
        assert permission.has_permission(request, None) is True
    
    def test_estudiante_no_permission(self, estudiante_factory):
        """Estudiante no debe tener permiso."""
        estudiante = estudiante_factory()
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = estudiante
        
        permission = IsCoordinador()
        assert permission.has_permission(request, None) is False
    
    def test_profesor_no_permission(self, profesor_factory):
        """Profesor no debe tener permiso."""
        profesor = profesor_factory()
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = profesor
        
        permission = IsCoordinador()
        assert permission.has_permission(request, None) is False


class TestIsCoordinadorOrProfesorPermission:
    """Pruebas para el permiso IsCoordinadorOrProfesor."""
    
    def test_coordinador_has_permission(self, coordinador_factory):
        """Coordinador debe tener permiso."""
        coordinador = coordinador_factory()
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = coordinador
        
        permission = IsCoordinadorOrProfesor()
        assert permission.has_permission(request, None) is True
    
    def test_profesor_has_permission(self, profesor_factory):
        """Profesor debe tener permiso."""
        profesor = profesor_factory()
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = profesor
        
        permission = IsCoordinadorOrProfesor()
        assert permission.has_permission(request, None) is True
    
    def test_estudiante_no_permission(self, estudiante_factory):
        """Estudiante no debe tener permiso."""
        estudiante = estudiante_factory()
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = estudiante
        
        permission = IsCoordinadorOrProfesor()
        assert permission.has_permission(request, None) is False
