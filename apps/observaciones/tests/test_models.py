"""
Tests para los modelos del módulo de observaciones.
RF-014: Observaciones del Profesor
"""
import pytest
from apps.observaciones.models import Observacion
from apps.observaciones.factories import ObservacionFactory
from apps.practicas.factories import PracticaFactory
from apps.usuarios.factories import ProfesorFactory


@pytest.mark.django_db
class TestObservacionModel:
    """Tests para el modelo Observacion."""
    
    def test_create_observacion(self):
        """Test crear observación."""
        observacion = ObservacionFactory()
        assert observacion.pk is not None
        assert observacion.practica is not None
        assert observacion.profesor is not None
        assert observacion.texto != ''
    
    def test_observacion_str_representation(self):
        """Test representación en string."""
        observacion = ObservacionFactory()
        # El modelo no define __str__, debe retornar repr por defecto
        assert 'Observacion' in str(observacion)
    
    def test_observacion_con_texto_largo(self):
        """Test observación con texto largo."""
        texto_largo = 'Esta es una observación muy detallada. ' * 20
        observacion = ObservacionFactory(texto=texto_largo)
        assert observacion.texto == texto_largo
    
    def test_observacion_created_at(self):
        """Test campo created_at."""
        observacion = ObservacionFactory()
        assert observacion.created_at is not None


@pytest.mark.django_db
class TestObservacionRelaciones:
    """Tests para relaciones del modelo Observacion."""
    
    def test_observacion_tiene_practica(self):
        """Test observación tiene práctica asociada."""
        practica = PracticaFactory()
        observacion = ObservacionFactory(practica=practica)
        
        assert observacion.practica == practica
        assert observacion in practica.observaciones.all()
    
    def test_observacion_tiene_profesor(self):
        """Test observación tiene profesor asociado."""
        profesor = ProfesorFactory()
        observacion = ObservacionFactory(profesor=profesor)
        
        assert observacion.profesor == profesor
    
    def test_practica_puede_tener_multiples_observaciones(self):
        """Test una práctica puede tener múltiples observaciones."""
        practica = PracticaFactory()
        ObservacionFactory.create_batch(3, practica=practica)
        
        assert practica.observaciones.count() == 3
    
    def test_profesor_puede_crear_multiples_observaciones(self):
        """Test un profesor puede crear múltiples observaciones."""
        profesor = ProfesorFactory()
        observaciones = ObservacionFactory.create_batch(5, profesor=profesor)
        
        assert len(observaciones) == 5
        for obs in observaciones:
            assert obs.profesor == profesor


@pytest.mark.django_db
class TestObservacionOrdenamiento:
    """Tests para ordenamiento de observaciones."""
    
    def test_observaciones_ordenadas_por_fecha_descendente(self):
        """Test observaciones ordenadas por fecha (más reciente primero)."""
        practica = PracticaFactory()
        obs1 = ObservacionFactory(practica=practica)
        obs2 = ObservacionFactory(practica=practica)
        obs3 = ObservacionFactory(practica=practica)
        
        observaciones = Observacion.objects.filter(practica=practica)
        # Verificar que están ordenadas por created_at descendente (Meta ordering)
        assert observaciones.count() == 3
        # La más reciente debe ser la última creada
        assert observaciones.first().pk == obs3.pk


@pytest.mark.django_db
class TestObservacionQuerysets:
    """Tests para querysets de observaciones."""
    
    def test_filter_observaciones_por_practica(self):
        """Test filtrar observaciones por práctica."""
        practica1 = PracticaFactory()
        practica2 = PracticaFactory()
        
        ObservacionFactory.create_batch(3, practica=practica1)
        ObservacionFactory.create_batch(2, practica=practica2)
        
        obs_practica1 = Observacion.objects.filter(practica=practica1)
        obs_practica2 = Observacion.objects.filter(practica=practica2)
        
        assert obs_practica1.count() == 3
        assert obs_practica2.count() == 2
    
    def test_filter_observaciones_por_profesor(self):
        """Test filtrar observaciones por profesor."""
        profesor1 = ProfesorFactory()
        profesor2 = ProfesorFactory()
        
        ObservacionFactory.create_batch(4, profesor=profesor1)
        ObservacionFactory.create_batch(1, profesor=profesor2)
        
        obs_profesor1 = Observacion.objects.filter(profesor=profesor1)
        obs_profesor2 = Observacion.objects.filter(profesor=profesor2)
        
        assert obs_profesor1.count() == 4
        assert obs_profesor2.count() == 1
    
    def test_buscar_observacion_por_texto(self):
        """Test buscar observación por contenido de texto."""
        ObservacionFactory(texto='El estudiante muestra excelente desempeño')
        ObservacionFactory(texto='Necesita mejorar la puntualidad')
        ObservacionFactory(texto='Trabajo sobresaliente en el proyecto')
        
        observaciones_positivas = Observacion.objects.filter(
            texto__icontains='excelente'
        )
        
        assert observaciones_positivas.count() >= 1
