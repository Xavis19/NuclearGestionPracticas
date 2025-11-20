"""
Factories para el módulo de documentos.
"""
import factory
from factory import fuzzy
from django.core.files.uploadedfile import SimpleUploadedFile
import hashlib
from .models import Documento


class DocumentoFactory(factory.django.DjangoModelFactory):
    """Factory para crear documentos."""
    
    class Meta:
        model = Documento
    
    tipo = factory.Faker('random_element', elements=[
        'CV', 'Carta de Presentación', 'Certificado', 'Constancia',
        'Informe', 'Evaluación', 'Contrato', 'Convenio'
    ])
    file = factory.LazyAttribute(lambda obj: SimpleUploadedFile(
        f'{obj.tipo.lower().replace(" ", "_")}.pdf',
        b'PDF content here',
        content_type='application/pdf'
    ))
    hash = factory.LazyAttribute(lambda obj: hashlib.sha256(
        f'{obj.tipo}'.encode()
    ).hexdigest())
    valido = True


class DocumentoValidoFactory(DocumentoFactory):
    """Factory para documentos válidos."""
    valido = True


class DocumentoInvalidoFactory(DocumentoFactory):
    """Factory para documentos inválidos."""
    valido = False
