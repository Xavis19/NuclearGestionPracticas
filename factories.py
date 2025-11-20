"""
Factories adicionales para apps de prácticas.
"""
import factory
from factory.django import DjangoModelFactory
from factory import fuzzy
from datetime import datetime, timedelta
from django.utils import timezone

from apps.usuarios.factories import EstudianteFactory, ProfesorFactory, CoordinadorFactory


# Nota: Estas son factories de ejemplo para otras apps
# Puedes completarlas según tus modelos reales

class VacanteFactoryBase(DjangoModelFactory):
    """Factory base para Vacantes - ajustar según tu modelo real."""
    
    class Meta:
        model = 'vacantes.Vacante'  # Ajustar al modelo real
        abstract = True
    
    titulo = factory.Faker('job', locale='es_ES')
    descripcion = factory.Faker('text', max_nb_chars=500, locale='es_ES')
    empresa = factory.Faker('company', locale='es_ES')
    ubicacion = factory.Faker('city', locale='es_ES')
    fecha_inicio = factory.LazyFunction(lambda: timezone.now().date())
    fecha_fin = factory.LazyFunction(lambda: (timezone.now() + timedelta(days=90)).date())
    vacantes_disponibles = fuzzy.FuzzyInteger(1, 5)
    activa = True


class PostulacionFactoryBase(DjangoModelFactory):
    """Factory base para Postulaciones - ajustar según tu modelo real."""
    
    class Meta:
        model = 'postulaciones.Postulacion'  # Ajustar al modelo real
        abstract = True
    
    estudiante = factory.SubFactory(EstudianteFactory)
    # vacante = factory.SubFactory(VacanteFactory)
    fecha_postulacion = factory.LazyFunction(timezone.now)
    estado = 'PENDIENTE'


class PracticaFactoryBase(DjangoModelFactory):
    """Factory base para Prácticas - ajustar según tu modelo real."""
    
    class Meta:
        model = 'practicas.Practica'  # Ajustar al modelo real
        abstract = True
    
    estudiante = factory.SubFactory(EstudianteFactory)
    tutor_academico = factory.SubFactory(ProfesorFactory)
    fecha_inicio = factory.LazyFunction(lambda: timezone.now().date())
    fecha_fin = factory.LazyFunction(lambda: (timezone.now() + timedelta(days=180)).date())
    estado = 'ACTIVA'
