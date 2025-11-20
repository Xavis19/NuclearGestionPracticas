"""
Ejemplo de template de pruebas para otras apps.

Copia este archivo a apps/<tu_app>/tests/test_models.py 
y adapta según tus modelos.
"""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db


# ===========================================
# TEMPLATE: Pruebas de Modelos
# ===========================================

class TestMiModelo:
    """Pruebas para MiModelo."""
    
    def test_crear_instancia_basica(self):
        """Debe crear una instancia con valores por defecto."""
        # from apps.mi_app.models import MiModelo
        
        # instancia = MiModelo.objects.create(
        #     campo1='valor1',
        #     campo2='valor2'
        # )
        
        # assert instancia.pk is not None
        # assert instancia.campo1 == 'valor1'
        pass
    
    def test_str_representation(self):
        """La representación en string debe ser correcta."""
        # instancia = MiModelo.objects.create(nombre='Test')
        # assert str(instancia) == 'Test'
        pass
    
    def test_campo_unico(self):
        """Campos únicos deben generar error al duplicar."""
        # from django.db import IntegrityError
        
        # MiModelo.objects.create(codigo='ABC123')
        # with pytest.raises(IntegrityError):
        #     MiModelo.objects.create(codigo='ABC123')
        pass
    
    def test_relacion_con_usuario(self, estudiante_factory):
        """Debe relacionarse correctamente con Usuario."""
        # estudiante = estudiante_factory()
        
        # instancia = MiModelo.objects.create(
        #     estudiante=estudiante,
        #     otros_campos='...'
        # )
        
        # assert instancia.estudiante == estudiante
        pass


# ===========================================
# TEMPLATE: Pruebas de API/Views
# ===========================================

class TestMiModeloAPI:
    """Pruebas para la API de MiModelo."""
    
    def test_list_como_coordinador(self, coordinador_client):
        """Coordinador debe poder listar."""
        # from django.urls import reverse
        # from rest_framework import status
        
        # url = reverse('mimodelo-list')
        # response = coordinador_client.get(url)
        
        # assert response.status_code == status.HTTP_200_OK
        pass
    
    def test_create_como_coordinador(self, coordinador_client):
        """Coordinador debe poder crear."""
        # from django.urls import reverse
        # from rest_framework import status
        
        # url = reverse('mimodelo-list')
        # data = {
        #     'campo1': 'valor1',
        #     'campo2': 'valor2'
        # }
        
        # response = coordinador_client.post(url, data)
        
        # assert response.status_code == status.HTTP_201_CREATED
        pass
    
    def test_estudiante_sin_permiso(self, estudiante_client):
        """Estudiante no debe tener acceso."""
        # from django.urls import reverse
        # from rest_framework import status
        
        # url = reverse('mimodelo-list')
        # response = estudiante_client.get(url)
        
        # assert response.status_code == status.HTTP_403_FORBIDDEN
        pass


# ===========================================
# TEMPLATE: Pruebas de Serializers
# ===========================================

class TestMiModeloSerializer:
    """Pruebas para MiModeloSerializer."""
    
    def test_serialize(self):
        """Debe serializar correctamente."""
        # from apps.mi_app.serializers import MiModeloSerializer
        # from apps.mi_app.models import MiModelo
        
        # instancia = MiModelo.objects.create(campo='valor')
        # serializer = MiModeloSerializer(instancia)
        
        # assert serializer.data['campo'] == 'valor'
        pass
    
    def test_validacion(self):
        """Debe validar datos correctamente."""
        # from apps.mi_app.serializers import MiModeloSerializer
        
        # data = {'campo_requerido': 'valor'}
        # serializer = MiModeloSerializer(data=data)
        
        # assert serializer.is_valid()
        pass
    
    def test_validacion_falla(self):
        """Debe fallar con datos inválidos."""
        # from apps.mi_app.serializers import MiModeloSerializer
        
        # data = {}  # Falta campo requerido
        # serializer = MiModeloSerializer(data=data)
        
        # assert not serializer.is_valid()
        # assert 'campo_requerido' in serializer.errors
        pass


# ===========================================
# TEMPLATE: Pruebas de Factories
# ===========================================

class TestMiModeloFactory:
    """Pruebas para MiModeloFactory."""
    
    def test_factory_crea_instancia_valida(self):
        """Factory debe crear instancia válida."""
        # from apps.mi_app.factories import MiModeloFactory
        
        # instancia = MiModeloFactory()
        
        # assert instancia.pk is not None
        # assert instancia.campo1 is not None
        pass
    
    def test_factory_batch(self):
        """Debe crear múltiples instancias."""
        # from apps.mi_app.factories import MiModeloFactory
        # from apps.mi_app.models import MiModelo
        
        # instancias = MiModeloFactory.create_batch(5)
        
        # assert len(instancias) == 5
        # assert MiModelo.objects.count() == 5
        pass
