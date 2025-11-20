"""
Factories para generar datos de prueba de Postulaciones.
"""
import factory
from factory.django import DjangoModelFactory
from datetime import datetime
from django.utils import timezone

from apps.postulaciones.models import Postulacion
from apps.usuarios.factories import EstudianteFactory, CoordinadorFactory
from apps.vacantes.factories import VacanteFactory


class PostulacionFactory(DjangoModelFactory):
    """Factory para crear postulaciones."""
    
    class Meta:
        model = Postulacion
    
    estudiante = factory.SubFactory(EstudianteFactory)
    vacante = factory.SubFactory(VacanteFactory)
    estado = Postulacion.PENDIENTE
    motivacion = factory.Faker('text', max_nb_chars=300, locale='es_ES')


class PostulacionPendienteFactory(PostulacionFactory):
    """Factory para postulaciones pendientes."""
    estado = Postulacion.PENDIENTE


class PostulacionSeleccionadaFactory(PostulacionFactory):
    """Factory para postulaciones seleccionadas."""
    estado = Postulacion.SELECCIONADO
    fecha_seleccion = factory.LazyFunction(timezone.now)
    seleccionado_por = factory.SubFactory(CoordinadorFactory)


class PostulacionRechazadaFactory(PostulacionFactory):
    """Factory para postulaciones rechazadas."""
    estado = Postulacion.RECHAZADO
    fecha_seleccion = factory.LazyFunction(timezone.now)
    seleccionado_por = factory.SubFactory(CoordinadorFactory)
