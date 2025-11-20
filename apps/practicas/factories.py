"""
Factories para generar datos de prueba de Prácticas.
"""
import factory
from factory.django import DjangoModelFactory
from factory import fuzzy
from datetime import date, timedelta
from django.utils import timezone

from apps.practicas.models import Practica
from apps.usuarios.factories import EstudianteFactory, ProfesorFactory
from apps.vacantes.factories import EmpresaFactory


class PracticaFactory(factory.django.DjangoModelFactory):
    """Factory para crear prácticas."""
    
    class Meta:
        model = Practica
    
    estudiante = factory.SubFactory('apps.usuarios.factories.EstudianteFactory')
    profesor = factory.SubFactory('apps.usuarios.factories.ProfesorFactory')
    empresa = factory.SubFactory('apps.vacantes.factories.EmpresaFactory')
    area_practica = factory.Faker('job', locale='es_ES')
    proyecto = factory.Faker('text', max_nb_chars=200, locale='es_ES')
    fecha_inicio = factory.LazyFunction(date.today)
    fecha_fin = factory.LazyFunction(lambda: date.today() + timedelta(days=120))
    estado = Practica.PENDIENTE
    cerrada = False
    calificacion_final = None
    asignada_por = factory.SubFactory('apps.usuarios.factories.CoordinadorFactory')


class PracticaPendienteFactory(PracticaFactory):
    """Factory para prácticas pendientes."""
    estado = Practica.PENDIENTE
    profesor = None
    empresa = None


class PracticaAsignadaFactory(PracticaFactory):
    """Factory para prácticas asignadas."""
    estado = Practica.ASIGNADA


class PracticaEnCursoFactory(PracticaFactory):
    """Factory para prácticas en curso."""
    estado = Practica.EN_CURSO


class PracticaCompletadaFactory(PracticaFactory):
    """Factory para prácticas completadas."""
    estado = Practica.COMPLETADA
    fecha_fin = factory.LazyFunction(lambda: date.today() - timedelta(days=1))
