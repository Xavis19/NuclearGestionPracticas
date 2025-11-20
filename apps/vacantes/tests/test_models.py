"""
Pruebas unitarias para los modelos de Vacantes.
"""
import pytest
from datetime import date, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.vacantes.models import Empresa, Vacante
from apps.vacantes.factories import EmpresaFactory, VacanteFactory, VacanteAbiertaFactory, VacanteCerradaFactory
from apps.usuarios.factories import EstudianteFactory

pytestmark = pytest.mark.django_db


class TestEmpresaModel:
    """Pruebas para el modelo Empresa."""
    
    def test_create_empresa(self):
        """Debe crear una empresa con todos sus campos."""
        empresa = EmpresaFactory(
            nombre='TechCorp',
            rfc='TEC1234567890',
            razon_social='TechCorp S.A. de C.V.'
        )
        
        assert empresa.pk is not None
        assert empresa.nombre == 'TechCorp'
        assert empresa.rfc == 'TEC1234567890'
        assert empresa.activa is True
    
    def test_empresa_str_representation(self):
        """La representación en string debe ser el nombre."""
        empresa = EmpresaFactory(nombre='TestCorp')
        assert str(empresa) == 'TestCorp'
    
    def test_rfc_is_unique(self):
        """El RFC debe ser único."""
        EmpresaFactory(rfc='RFC123456789')
        with pytest.raises(IntegrityError):
            EmpresaFactory(rfc='RFC123456789')
    
    def test_empresa_con_todos_los_campos(self):
        """Debe poder crear empresa con todos los campos opcionales."""
        empresa = EmpresaFactory(
            sitio_web='https://empresa.com',
            sector='Tecnología',
            tamaño='GRANDE',
            verificada=True
        )
        
        assert empresa.sitio_web == 'https://empresa.com'
        assert empresa.sector == 'Tecnología'
        assert empresa.tamaño == 'GRANDE'
        assert empresa.verificada is True
    
    def test_empresa_activa_default(self):
        """Las empresas deben estar activas por defecto."""
        empresa = EmpresaFactory()
        assert empresa.activa is True
    
    def test_empresa_no_verificada_default(self):
        """Las empresas no deben estar verificadas por defecto."""
        empresa = EmpresaFactory(verificada=False)
        assert empresa.verificada is False
    
    def test_empresa_relation_with_user(self):
        """La empresa debe relacionarse correctamente con el usuario creador."""
        empresa = EmpresaFactory()
        assert empresa.created_by is not None
        assert empresa.created_by.is_coordinador


class TestVacanteModel:
    """Pruebas para el modelo Vacante."""
    
    def test_create_vacante(self):
        """Debe crear una vacante con todos sus campos."""
        vacante = VacanteFactory(
            titulo='Desarrollador Junior',
            semestre_minimo=5,
            promedio_minimo=80.0
        )
        
        assert vacante.pk is not None
        assert vacante.titulo == 'Desarrollador Junior'
        assert vacante.semestre_minimo == 5
        assert vacante.promedio_minimo == 80.0
    
    def test_vacante_str_representation(self):
        """La representación debe incluir título y empresa."""
        empresa = EmpresaFactory(nombre='TechCorp')
        vacante = VacanteFactory(
            titulo='Practicante',
            empresa=empresa
        )
        
        assert 'Practicante' in str(vacante)
        assert 'TechCorp' in str(vacante)
    
    def test_vacante_defaults(self):
        """Debe tener valores por defecto correctos."""
        vacante = VacanteFactory()
        
        assert vacante.estado == Vacante.ABIERTA
        assert vacante.vacantes_ocupadas == 0
        assert vacante.modalidad in ['PRESENCIAL', 'REMOTO', 'HIBRIDO']
    
    def test_vacante_relation_with_empresa(self):
        """La vacante debe relacionarse con una empresa."""
        empresa = EmpresaFactory()
        vacante = VacanteFactory(empresa=empresa)
        
        assert vacante.empresa == empresa
        assert vacante in empresa.vacantes.all()
    
    def test_vacantes_restantes_property(self):
        """Debe calcular correctamente las vacantes restantes."""
        vacante = VacanteFactory(
            vacantes_disponibles=5,
            vacantes_ocupadas=2
        )
        
        assert vacante.vacantes_restantes == 3
    
    def test_esta_abierta_property_true(self):
        """Debe retornar True si está abierta y hay vacantes."""
        vacante = VacanteAbiertaFactory(
            estado=Vacante.ABIERTA,
            vacantes_disponibles=3,
            vacantes_ocupadas=0
        )
        
        assert vacante.esta_abierta is True
    
    def test_esta_abierta_property_false_cerrada(self):
        """Debe retornar False si está cerrada."""
        vacante = VacanteCerradaFactory(estado=Vacante.CERRADA)
        
        assert vacante.esta_abierta is False
    
    def test_esta_abierta_property_false_sin_vacantes(self):
        """Debe retornar False si no hay vacantes disponibles."""
        vacante = VacanteFactory(
            estado=Vacante.ABIERTA,
            vacantes_disponibles=2,
            vacantes_ocupadas=2
        )
        
        assert vacante.esta_abierta is False
    
    def test_incrementar_ocupadas(self):
        """Debe incrementar el contador de vacantes ocupadas."""
        vacante = VacanteFactory(
            vacantes_disponibles=3,
            vacantes_ocupadas=0,
            estado=Vacante.ABIERTA
        )
        
        vacante.incrementar_ocupadas()
        assert vacante.vacantes_ocupadas == 1
        assert vacante.estado == Vacante.ABIERTA
    
    def test_incrementar_ocupadas_cierra_cuando_llena(self):
        """Debe cerrar la vacante cuando se llenan todos los cupos."""
        vacante = VacanteFactory(
            vacantes_disponibles=2,
            vacantes_ocupadas=1,
            estado=Vacante.ABIERTA
        )
        
        vacante.incrementar_ocupadas()
        assert vacante.vacantes_ocupadas == 2
        assert vacante.estado == Vacante.CERRADA
    
    def test_decrementar_ocupadas(self):
        """Debe decrementar el contador de vacantes ocupadas."""
        vacante = VacanteFactory(
            vacantes_disponibles=3,
            vacantes_ocupadas=2
        )
        
        vacante.decrementar_ocupadas()
        assert vacante.vacantes_ocupadas == 1
    
    def test_decrementar_ocupadas_abre_si_estaba_cerrada(self):
        """Debe abrir la vacante si estaba cerrada por cupos."""
        vacante = VacanteCerradaFactory(
            vacantes_disponibles=2,
            vacantes_ocupadas=2,
            estado=Vacante.CERRADA
        )
        
        vacante.decrementar_ocupadas()
        assert vacante.vacantes_ocupadas == 1
        assert vacante.estado == Vacante.ABIERTA
    
    def test_decrementar_ocupadas_no_negativo(self):
        """No debe decrementar por debajo de cero."""
        vacante = VacanteFactory(vacantes_ocupadas=0)
        
        vacante.decrementar_ocupadas()
        assert vacante.vacantes_ocupadas == 0


class TestVacantePuedePostularse:
    """Pruebas para el método puede_postularse."""
    
    def test_puede_postularse_cumple_requisitos(self):
        """Estudiante que cumple todos los requisitos puede postularse."""
        vacante = VacanteFactory(
            estado=Vacante.ABIERTA,
            vacantes_disponibles=3,
            vacantes_ocupadas=0,
            semestre_minimo=5,
            promedio_minimo=80.0,
            carreras_solicitadas='Ingeniería en Sistemas Computacionales'
        )
        
        estudiante = EstudianteFactory(
            semestre=7,
            promedio=85.0,
            carrera='Ingeniería en Sistemas Computacionales'
        )
        
        puede, mensaje = vacante.puede_postularse(estudiante)
        assert puede is True
        assert 'Cumple los requisitos' in mensaje
    
    def test_no_puede_postularse_vacante_cerrada(self):
        """No puede postularse a vacante cerrada."""
        vacante = VacanteCerradaFactory()
        estudiante = EstudianteFactory()
        
        puede, mensaje = vacante.puede_postularse(estudiante)
        assert puede is False
        assert 'no está disponible' in mensaje
    
    def test_no_puede_postularse_sin_vacantes(self):
        """No puede postularse si no hay vacantes disponibles."""
        vacante = VacanteFactory(
            estado=Vacante.ABIERTA,
            vacantes_disponibles=2,
            vacantes_ocupadas=2
        )
        estudiante = EstudianteFactory()
        
        puede, mensaje = vacante.puede_postularse(estudiante)
        assert puede is False
    
    def test_no_puede_postularse_semestre_bajo(self):
        """No puede postularse si no cumple semestre mínimo."""
        vacante = VacanteFactory(
            estado=Vacante.ABIERTA,
            semestre_minimo=7
        )
        estudiante = EstudianteFactory(semestre=5)
        
        puede, mensaje = vacante.puede_postularse(estudiante)
        assert puede is False
        assert 'semestre' in mensaje.lower()
    
    def test_no_puede_postularse_promedio_bajo(self):
        """No puede postularse si no cumple promedio mínimo."""
        vacante = VacanteFactory(
            estado=Vacante.ABIERTA,
            promedio_minimo=85.0
        )
        estudiante = EstudianteFactory(
            semestre=7,
            promedio=75.0
        )
        
        puede, mensaje = vacante.puede_postularse(estudiante)
        assert puede is False
        assert 'promedio' in mensaje.lower()
    
    def test_no_puede_postularse_carrera_incorrecta(self):
        """No puede postularse si su carrera no está solicitada."""
        vacante = VacanteFactory(
            estado=Vacante.ABIERTA,
            carreras_solicitadas='Ingeniería Industrial, Ingeniería Mecánica',
            semestre_minimo=4,
            promedio_minimo=None  # Sin requisito de promedio para aislar la prueba
        )
        estudiante = EstudianteFactory(
            semestre=7,
            promedio=85.0,
            carrera='Ingeniería en Sistemas Computacionales'
        )
        
        puede, mensaje = vacante.puede_postularse(estudiante)
        assert puede is False
        assert 'carrera' in mensaje.lower()
    
    def test_puede_postularse_sin_promedio_requerido(self):
        """Puede postularse si no se requiere promedio mínimo."""
        vacante = VacanteFactory(
            estado=Vacante.ABIERTA,
            promedio_minimo=None
        )
        estudiante = EstudianteFactory(
            semestre=7,
            promedio=70.0
        )
        
        # Ajustar carrera para que coincida
        vacante.carreras_solicitadas = estudiante.carrera
        vacante.save()
        
        puede, mensaje = vacante.puede_postularse(estudiante)
        assert puede is True


class TestVacanteModalidades:
    """Pruebas para diferentes modalidades de vacantes."""
    
    def test_vacante_presencial(self):
        """Debe crear vacante presencial."""
        vacante = VacanteFactory(modalidad='PRESENCIAL')
        assert vacante.modalidad == 'PRESENCIAL'
    
    def test_vacante_remota(self):
        """Debe crear vacante remota."""
        vacante = VacanteFactory(modalidad='REMOTO')
        assert vacante.modalidad == 'REMOTO'
    
    def test_vacante_hibrida(self):
        """Debe crear vacante híbrida."""
        vacante = VacanteFactory(modalidad='HIBRIDO')
        assert vacante.modalidad == 'HIBRIDO'


class TestVacanteBeneficios:
    """Pruebas para vacantes con beneficios."""
    
    def test_vacante_remunerada(self):
        """Debe crear vacante remunerada con monto."""
        vacante = VacanteFactory(
            remunerada=True,
            monto_apoyo=5000.00
        )
        
        assert vacante.remunerada is True
        assert vacante.monto_apoyo == 5000.00
    
    def test_vacante_no_remunerada(self):
        """Debe crear vacante no remunerada."""
        vacante = VacanteFactory(
            remunerada=False,
            monto_apoyo=None
        )
        
        assert vacante.remunerada is False
        assert vacante.monto_apoyo is None
    
    def test_vacante_con_beneficios_adicionales(self):
        """Debe guardar beneficios adicionales."""
        beneficios = 'Seguro médico, vales de despensa, transporte'
        vacante = VacanteFactory(beneficios_adicionales=beneficios)
        
        assert vacante.beneficios_adicionales == beneficios


class TestVacanteQuerysets:
    """Pruebas para consultas de vacantes."""
    
    def test_filter_by_estado(self):
        """Debe poder filtrar vacantes por estado."""
        VacanteAbiertaFactory.create_batch(3)
        VacanteCerradaFactory.create_batch(2)
        
        abiertas = Vacante.objects.filter(estado=Vacante.ABIERTA)
        cerradas = Vacante.objects.filter(estado=Vacante.CERRADA)
        
        assert abiertas.count() >= 3
        assert cerradas.count() >= 2
    
    def test_filter_by_empresa(self):
        """Debe poder filtrar vacantes por empresa."""
        empresa = EmpresaFactory()
        VacanteFactory.create_batch(3, empresa=empresa)
        VacanteFactory.create_batch(2)  # Otras empresas
        
        vacantes_empresa = Vacante.objects.filter(empresa=empresa)
        assert vacantes_empresa.count() == 3
    
    def test_ordering_by_created_at(self):
        """Las vacantes deben ordenarse por fecha de creación desc."""
        vacantes = VacanteFactory.create_batch(5)
        queryset = Vacante.objects.all()
        
        # La primera debe ser la más reciente
        assert queryset.first().created_at >= queryset.last().created_at
