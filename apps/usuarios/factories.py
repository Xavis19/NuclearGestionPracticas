"""
Factories para generar datos de prueba usando Factory Boy.
"""
import factory
from factory.django import DjangoModelFactory
from factory import fuzzy
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker('es_ES')
User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory base para crear usuarios."""
    
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name', locale='es_ES')
    last_name = factory.Faker('last_name', locale='es_ES')
    phone = factory.Faker('phone_number', locale='es_ES')
    is_active = True
    is_staff = False
    is_superuser = False
    
    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        """Establecer password después de crear el objeto."""
        if not create:
            return
        
        if extracted:
            obj.set_password(extracted)
        else:
            obj.set_password('testpass123')


class EstudianteFactory(UserFactory):
    """Factory para crear estudiantes."""
    
    role = User.ESTUDIANTE
    matricula = factory.Sequence(lambda n: f'EST{n:08d}')
    carrera = factory.Faker('random_element', elements=[
        'Ingeniería en Sistemas Computacionales',
        'Ingeniería Industrial',
        'Ingeniería Electrónica',
        'Ingeniería Mecánica',
        'Contador Público',
    ])
    semestre = fuzzy.FuzzyInteger(1, 10)
    promedio = fuzzy.FuzzyDecimal(70.00, 100.00, precision=2)


class ProfesorFactory(UserFactory):
    """Factory para crear profesores."""
    
    role = User.PROFESOR
    departamento = factory.Faker('random_element', elements=[
        'Sistemas y Computación',
        'Ciencias Básicas',
        'Industrial',
        'Electrónica',
        'Ciencias Económico Administrativas',
    ])
    especialidad = factory.Faker('random_element', elements=[
        'Desarrollo de Software',
        'Redes y Telecomunicaciones',
        'Inteligencia Artificial',
        'Base de Datos',
        'Seguridad Informática',
    ])


class CoordinadorFactory(UserFactory):
    """Factory para crear coordinadores."""
    
    role = User.COORDINADOR
    is_staff = True
    departamento = 'Vinculación'
    especialidad = 'Coordinación de Prácticas Profesionales'


class SuperUserFactory(UserFactory):
    """Factory para crear superusuarios."""
    
    role = User.COORDINADOR
    is_staff = True
    is_superuser = True
    username = 'admin'
    email = 'admin@example.com'
