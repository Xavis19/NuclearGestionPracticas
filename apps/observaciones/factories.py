"""
Factories para el módulo de observaciones.
"""
import factory
from .models import Observacion


class ObservacionFactory(factory.django.DjangoModelFactory):
    """Factory para crear observaciones."""
    
    class Meta:
        model = Observacion
    
    practica = factory.SubFactory('apps.practicas.factories.PracticaFactory')
    profesor = factory.SubFactory('apps.usuarios.factories.ProfesorFactory')
    texto = factory.Faker('text', max_nb_chars=500, locale='es_ES')
