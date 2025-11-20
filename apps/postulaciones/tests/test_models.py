"""
Pruebas unitarias para el modelo de Postulaciones.
"""
import pytest
from django.db import IntegrityError
from django.utils import timezone

from apps.postulaciones.models import Postulacion
from apps.postulaciones.factories import (
    PostulacionFactory,
    PostulacionPendienteFactory,
    PostulacionSeleccionadaFactory,
    PostulacionRechazadaFactory
)
from apps.usuarios.factories import EstudianteFactory, CoordinadorFactory
from apps.vacantes.factories import VacanteFactory

pytestmark = pytest.mark.django_db


class TestPostulacionModel:
    """Pruebas para el modelo Postulacion."""
    
    def test_create_postulacion(self):
        """Debe crear una postulación con todos sus campos."""
        postulacion = PostulacionFactory(
            motivacion='Estoy muy interesado en esta práctica'
        )
        
        assert postulacion.pk is not None
        assert postulacion.estudiante is not None
        assert postulacion.vacante is not None
        assert postulacion.estado == Postulacion.PENDIENTE
        assert postulacion.motivacion is not None
    
    def test_postulacion_str_representation(self):
        """La representación en string debe incluir estudiante y vacante."""
        postulacion = PostulacionFactory()
        string_repr = str(postulacion)
        
        assert postulacion.estudiante.get_full_name() in string_repr
        assert postulacion.vacante.titulo in string_repr
    
    def test_postulacion_unique_constraint(self):
        """No se puede postular dos veces a la misma vacante."""
        estudiante = EstudianteFactory()
        vacante = VacanteFactory()
        
        PostulacionFactory(estudiante=estudiante, vacante=vacante)
        
        with pytest.raises(IntegrityError):
            PostulacionFactory(estudiante=estudiante, vacante=vacante)
    
    def test_postulacion_default_estado(self):
        """El estado por defecto debe ser PENDIENTE."""
        postulacion = PostulacionFactory()
        assert postulacion.estado == Postulacion.PENDIENTE
    
    def test_postulacion_fecha_seleccion_null(self):
        """Fecha de selección debe ser null para pendientes."""
        postulacion = PostulacionPendienteFactory()
        assert postulacion.fecha_seleccion is None
        assert postulacion.seleccionado_por is None


class TestPostulacionEstados:
    """Pruebas para los diferentes estados de postulación."""
    
    def test_postulacion_pendiente(self):
        """Debe crear postulación en estado pendiente."""
        postulacion = PostulacionPendienteFactory()
        
        assert postulacion.estado == Postulacion.PENDIENTE
        assert postulacion.fecha_seleccion is None
    
    def test_postulacion_seleccionada(self):
        """Debe crear postulación seleccionada."""
        postulacion = PostulacionSeleccionadaFactory()
        
        assert postulacion.estado == Postulacion.SELECCIONADO
        assert postulacion.fecha_seleccion is not None
        assert postulacion.seleccionado_por is not None
    
    def test_postulacion_rechazada(self):
        """Debe crear postulación rechazada."""
        postulacion = PostulacionRechazadaFactory()
        
        assert postulacion.estado == Postulacion.RECHAZADO
        assert postulacion.fecha_seleccion is not None
        assert postulacion.seleccionado_por is not None
    
    def test_cambiar_estado_a_seleccionado(self):
        """Debe poder cambiar estado de pendiente a seleccionado."""
        postulacion = PostulacionPendienteFactory()
        coordinador = CoordinadorFactory()
        
        postulacion.estado = Postulacion.SELECCIONADO
        postulacion.fecha_seleccion = timezone.now()
        postulacion.seleccionado_por = coordinador
        postulacion.save()
        
        postulacion.refresh_from_db()
        assert postulacion.estado == Postulacion.SELECCIONADO
        assert postulacion.seleccionado_por == coordinador


class TestPostulacionRelaciones:
    """Pruebas para las relaciones del modelo."""
    
    def test_relacion_con_estudiante(self):
        """Debe relacionarse correctamente con estudiante."""
        estudiante = EstudianteFactory()
        postulacion = PostulacionFactory(estudiante=estudiante)
        
        assert postulacion.estudiante == estudiante
        assert postulacion in estudiante.postulaciones.all()
    
    def test_relacion_con_vacante(self):
        """Debe relacionarse correctamente con vacante."""
        vacante = VacanteFactory()
        postulacion = PostulacionFactory(vacante=vacante)
        
        assert postulacion.vacante == vacante
        assert postulacion in vacante.postulaciones.all()
    
    def test_multiple_postulaciones_por_estudiante(self):
        """Un estudiante puede tener múltiples postulaciones."""
        estudiante = EstudianteFactory()
        
        postulacion1 = PostulacionFactory(estudiante=estudiante)
        postulacion2 = PostulacionFactory(estudiante=estudiante)
        
        assert estudiante.postulaciones.count() == 2
    
    def test_multiple_postulaciones_por_vacante(self):
        """Una vacante puede tener múltiples postulaciones."""
        vacante = VacanteFactory()
        
        PostulacionFactory.create_batch(3, vacante=vacante)
        
        assert vacante.postulaciones.count() == 3


class TestPostulacionQuerysets:
    """Pruebas para consultas de postulaciones."""
    
    def test_filter_by_estado(self):
        """Debe poder filtrar por estado."""
        PostulacionPendienteFactory.create_batch(3)
        PostulacionSeleccionadaFactory.create_batch(2)
        PostulacionRechazadaFactory.create_batch(1)
        
        pendientes = Postulacion.objects.filter(estado=Postulacion.PENDIENTE)
        seleccionadas = Postulacion.objects.filter(estado=Postulacion.SELECCIONADO)
        
        assert pendientes.count() == 3
        assert seleccionadas.count() == 2
    
    def test_filter_by_estudiante(self):
        """Debe poder filtrar por estudiante."""
        estudiante = EstudianteFactory()
        PostulacionFactory.create_batch(3, estudiante=estudiante)
        PostulacionFactory.create_batch(2)  # Otras postulaciones
        
        postulaciones_estudiante = Postulacion.objects.filter(estudiante=estudiante)
        assert postulaciones_estudiante.count() == 3
    
    def test_ordering_by_created_at(self):
        """Debe ordenar por fecha de creación descendente."""
        postulaciones = PostulacionFactory.create_batch(3)
        queryset = Postulacion.objects.all()
        
        assert queryset.first().created_at >= queryset.last().created_at
