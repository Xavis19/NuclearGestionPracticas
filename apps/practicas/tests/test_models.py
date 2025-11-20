"""
Pruebas unitarias para el modelo de Prácticas.
"""
import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError

from apps.practicas.models import Practica
from apps.practicas.factories import (
    PracticaFactory,
    PracticaPendienteFactory,
    PracticaAsignadaFactory,
    PracticaEnCursoFactory,
    PracticaCompletadaFactory
)
from apps.usuarios.factories import EstudianteFactory, ProfesorFactory
from apps.vacantes.factories import EmpresaFactory

pytestmark = pytest.mark.django_db


class TestPracticaModel:
    """Pruebas para el modelo Practica."""
    
    def test_create_practica(self):
        """Debe crear una práctica con todos sus campos."""
        practica = PracticaFactory(
            area_practica='Desarrollo de Software'
        )
        
        assert practica.pk is not None
        assert practica.estudiante is not None
        assert practica.estado == Practica.PENDIENTE
    
    def test_practica_str_representation(self):
        """La representación en string debe incluir estudiante y empresa."""
        practica = PracticaFactory()
        string_repr = str(practica)
        
        assert practica.estudiante.get_full_name() in string_repr
    
    def test_practica_con_profesor_asignado(self):
        """Debe poder asignar un profesor."""
        profesor = ProfesorFactory()
        practica = PracticaFactory(profesor=profesor)
        
        assert practica.profesor == profesor
        assert practica in profesor.practicas_supervisadas.all()
    
    def test_practica_con_empresa_asignada(self):
        """Debe poder asignar una empresa."""
        empresa = EmpresaFactory()
        practica = PracticaFactory(empresa=empresa)
        
        assert practica.empresa == empresa
        assert practica in empresa.practicas.all()


class TestPracticaEstados:
    """Pruebas para los diferentes estados de práctica."""
    
    def test_practica_pendiente(self):
        """Debe crear práctica pendiente sin asignaciones."""
        practica = PracticaPendienteFactory()
        
        assert practica.estado == Practica.PENDIENTE
        assert practica.profesor is None
        assert practica.empresa is None
    
    def test_practica_asignada(self):
        """Debe crear práctica asignada."""
        practica = PracticaAsignadaFactory()
        
        assert practica.estado == Practica.ASIGNADA
        assert practica.profesor is not None
        assert practica.empresa is not None
    
    def test_practica_en_curso(self):
        """Debe crear práctica en curso."""
        practica = PracticaEnCursoFactory()
        
        assert practica.estado == Practica.EN_CURSO
    
    def test_practica_completada(self):
        """Debe crear práctica completada."""
        practica = PracticaCompletadaFactory()
        
        assert practica.estado == Practica.COMPLETADA
    
    def test_cambiar_estado_practica(self):
        """Debe poder cambiar el estado de una práctica."""
        practica = PracticaPendienteFactory()
        
        practica.estado = Practica.ASIGNADA
        practica.save()
        
        practica.refresh_from_db()
        assert practica.estado == Practica.ASIGNADA


class TestPracticaFechas:
    """Pruebas para las fechas de práctica."""
    
    def test_practica_con_fechas(self):
        """Debe tener fechas de inicio y fin."""
        inicio = date.today()
        fin = inicio + timedelta(days=180)
        
        practica = PracticaFactory(
            fecha_inicio=inicio,
            fecha_fin=fin
        )
        
        assert practica.fecha_inicio == inicio
        assert practica.fecha_fin == fin
    
    def test_duracion_practica(self):
        """La fecha fin debe ser posterior a la de inicio."""
        practica = PracticaFactory()
        
        if practica.fecha_inicio and practica.fecha_fin:
            assert practica.fecha_fin > practica.fecha_inicio


class TestPracticaRelaciones:
    """Pruebas para las relaciones del modelo."""
    
    def test_estudiante_puede_tener_multiples_practicas(self):
        """Un estudiante puede tener múltiples prácticas."""
        estudiante = EstudianteFactory()
        
        PracticaFactory.create_batch(3, estudiante=estudiante)
        
        assert estudiante.practicas.count() == 3
    
    def test_profesor_puede_supervisar_multiples_practicas(self):
        """Un profesor puede supervisar múltiples prácticas."""
        profesor = ProfesorFactory()
        
        PracticaFactory.create_batch(5, profesor=profesor)
        
        assert profesor.practicas_supervisadas.count() == 5


class TestPracticaQuerysets:
    """Pruebas para consultas de prácticas."""
    
    def test_filter_by_estado(self):
        """Debe poder filtrar por estado."""
        PracticaPendienteFactory.create_batch(2)
        PracticaEnCursoFactory.create_batch(3)
        PracticaCompletadaFactory.create_batch(1)
        
        en_curso = Practica.objects.filter(estado=Practica.EN_CURSO)
        assert en_curso.count() == 3
    
    def test_filter_by_estudiante(self):
        """Debe poder filtrar por estudiante."""
        estudiante = EstudianteFactory()
        PracticaFactory.create_batch(2, estudiante=estudiante)
        PracticaFactory.create_batch(3)  # Otras prácticas
        
        practicas_estudiante = Practica.objects.filter(estudiante=estudiante)
        assert practicas_estudiante.count() == 2
    
    def test_filter_by_profesor(self):
        """Debe poder filtrar por profesor."""
        profesor = ProfesorFactory()
        PracticaFactory.create_batch(4, profesor=profesor)
        PracticaFactory.create_batch(2)  # Otras prácticas
        
        practicas_profesor = Practica.objects.filter(profesor=profesor)
        assert practicas_profesor.count() == 4
