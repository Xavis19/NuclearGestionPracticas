"""
Factories para generar datos de prueba de Vacantes.
"""
import factory
from factory.django import DjangoModelFactory
from factory import fuzzy
from datetime import date, timedelta
from django.utils import timezone

from apps.vacantes.models import Empresa, Vacante
from apps.usuarios.factories import CoordinadorFactory


class EmpresaFactory(DjangoModelFactory):
    """Factory para crear empresas."""
    
    class Meta:
        model = Empresa
    
    nombre = factory.Sequence(lambda n: f'Empresa {n}')
    rfc = factory.Sequence(lambda n: f'RFC{n:010d}XX')
    razon_social = factory.LazyAttribute(lambda obj: f'{obj.nombre} S.A. de C.V.')
    
    # Información de contacto
    direccion = factory.Faker('address', locale='es_MX')
    telefono = factory.Faker('phone_number', locale='es_MX')
    email = factory.LazyAttribute(lambda obj: f'{obj.nombre.replace(" ", "").lower()}@empresa.com')
    sitio_web = factory.LazyAttribute(lambda obj: f'https://www.{obj.nombre.replace(" ", "").lower()}.com')
    
    # Contacto principal
    contacto_nombre = factory.Faker('name', locale='es_ES')
    contacto_puesto = factory.Faker('random_element', elements=[
        'Gerente de Recursos Humanos',
        'Director de Capital Humano',
        'Jefe de Reclutamiento',
        'Coordinador de Prácticas',
    ])
    contacto_email = factory.Faker('email', locale='es_ES')
    contacto_telefono = factory.Faker('phone_number', locale='es_MX')
    
    # Información adicional
    sector = factory.Faker('random_element', elements=[
        'Tecnología',
        'Manufactura',
        'Servicios',
        'Consultoría',
        'Financiero',
        'Educación',
        'Salud',
    ])
    tamaño = factory.Faker('random_element', elements=[
        'MICRO',
        'PEQUEÑA',
        'MEDIANA',
        'GRANDE',
    ])
    
    # Estado
    activa = True
    verificada = True
    
    # Metadata
    created_by = factory.SubFactory(CoordinadorFactory)


class VacanteFactory(DjangoModelFactory):
    """Factory para crear vacantes."""
    
    class Meta:
        model = Vacante
    
    empresa = factory.SubFactory(EmpresaFactory)
    titulo = factory.Faker('random_element', elements=[
        'Practicante de Desarrollo de Software',
        'Practicante de Ingeniería Industrial',
        'Practicante de Diseño Gráfico',
        'Practicante de Administración',
        'Practicante de Contabilidad',
        'Practicante de Marketing Digital',
        'Practicante de Recursos Humanos',
        'Practicante de Logística',
    ])
    descripcion = factory.Faker('text', max_nb_chars=500, locale='es_ES')
    
    # Requisitos
    requisitos = factory.LazyAttribute(lambda _: '\n'.join([
        '- Estudiante activo',
        '- Disponibilidad de tiempo completo',
        '- Conocimientos básicos de la materia',
        '- Actitud proactiva',
        '- Trabajo en equipo',
    ]))
    carreras_solicitadas = factory.Faker('random_element', elements=[
        'Ingeniería en Sistemas Computacionales',
        'Ingeniería Industrial',
        'Ingeniería Electrónica',
        'Contador Público',
        'Administración de Empresas',
    ])
    semestre_minimo = 4  # Semestre mínimo para prácticas profesionales
    promedio_minimo = fuzzy.FuzzyDecimal(75.00, 85.00, precision=2)
    
    # Detalles de la práctica
    area = factory.Faker('random_element', elements=[
        'Desarrollo de Software',
        'Producción',
        'Calidad',
        'Administración',
        'Contabilidad',
        'Marketing',
        'Recursos Humanos',
    ])
    modalidad = factory.Faker('random_element', elements=[
        'PRESENCIAL',
        'REMOTO',
        'HIBRIDO',
    ])
    ubicacion = factory.Faker('city', locale='es_MX')
    
    # Horario y duración
    horario = factory.Faker('random_element', elements=[
        'Lunes a Viernes 8:00 - 14:00',
        'Lunes a Viernes 9:00 - 15:00',
        'Lunes a Viernes 14:00 - 18:00',
        'Flexible',
    ])
    duracion_meses = fuzzy.FuzzyInteger(4, 6)
    
    # Cupos y fechas
    vacantes_disponibles = fuzzy.FuzzyInteger(1, 5)
    vacantes_ocupadas = 0
    fecha_inicio = factory.LazyFunction(lambda: (timezone.now() + timedelta(days=30)).date())
    fecha_cierre_convocatoria = factory.LazyFunction(lambda: (timezone.now() + timedelta(days=15)).date())
    
    # Beneficios
    remunerada = factory.Faker('boolean', chance_of_getting_true=60)
    monto_apoyo = factory.Maybe(
        'remunerada',
        yes_declaration=fuzzy.FuzzyDecimal(2000.00, 6000.00, precision=2),
        no_declaration=None
    )
    beneficios_adicionales = factory.Faker('random_element', elements=[
        'Seguro de gastos médicos menores',
        'Vales de despensa',
        'Transporte',
        'Comedor',
        None,
    ])
    
    # Estado
    estado = Vacante.ABIERTA
    
    # Metadata
    created_by = factory.SubFactory(CoordinadorFactory)


class VacanteAbiertaFactory(VacanteFactory):
    """Factory para vacantes abiertas."""
    estado = Vacante.ABIERTA
    vacantes_disponibles = 3
    vacantes_ocupadas = 0


class VacanteCerradaFactory(VacanteFactory):
    """Factory para vacantes cerradas."""
    estado = Vacante.CERRADA
    vacantes_disponibles = 2
    vacantes_ocupadas = 2


class VacantePausadaFactory(VacanteFactory):
    """Factory para vacantes pausadas."""
    estado = Vacante.PAUSADA


class VacanteRemoataFactory(VacanteFactory):
    """Factory para vacantes remotas."""
    modalidad = 'REMOTO'
    ubicacion = 'Remoto - Cualquier ubicación'


class VacanteRemuneradaFactory(VacanteFactory):
    """Factory para vacantes remuneradas."""
    remunerada = True
    monto_apoyo = fuzzy.FuzzyDecimal(3000.00, 8000.00, precision=2)
