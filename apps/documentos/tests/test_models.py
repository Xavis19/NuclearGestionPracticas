"""
Tests para los modelos del módulo de documentos.
RF-003: Documentación
"""
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.documentos.models import Documento
from apps.documentos.factories import (
    DocumentoFactory, DocumentoValidoFactory, DocumentoInvalidoFactory
)


@pytest.mark.django_db
class TestDocumentoModel:
    """Tests para el modelo Documento."""
    
    def test_create_documento(self):
        """Test crear documento."""
        documento = DocumentoFactory(tipo='CV')
        assert documento.pk is not None
        assert documento.tipo == 'CV'
        assert documento.valido is True
        assert documento.hash is not None
    
    def test_documento_str_representation(self):
        """Test representación en string."""
        documento = DocumentoFactory(tipo='Certificado')
        # El modelo no define __str__, debe retornar repr por defecto
        assert 'Documento' in str(documento)
    
    def test_documento_file_field(self):
        """Test campo de archivo."""
        documento = DocumentoFactory()
        assert documento.file is not None
        assert documento.file.name is not None
    
    def test_documento_hash_generation(self):
        """Test generación de hash."""
        documento = DocumentoFactory()
        assert documento.hash is not None
        assert len(documento.hash) == 64  # SHA256 hash length


@pytest.mark.django_db
class TestDocumentoValidacion:
    """Tests para validación de documentos."""
    
    def test_documento_valido(self):
        """Test documento válido."""
        documento = DocumentoValidoFactory()
        assert documento.valido is True
    
    def test_documento_invalido(self):
        """Test documento inválido."""
        documento = DocumentoInvalidoFactory()
        assert documento.valido is False
    
    def test_marcar_documento_como_invalido(self):
        """Test marcar documento como inválido."""
        documento = DocumentoValidoFactory()
        assert documento.valido is True
        
        documento.valido = False
        documento.save()
        documento.refresh_from_db()
        
        assert documento.valido is False


@pytest.mark.django_db
class TestDocumentoTipos:
    """Tests para tipos de documentos."""
    
    def test_tipos_documento_validos(self):
        """Test crear documentos de diferentes tipos."""
        tipos = ['CV', 'Certificado', 'Informe', 'Contrato']
        
        for tipo in tipos:
            documento = DocumentoFactory(tipo=tipo)
            assert documento.tipo == tipo
            assert documento.pk is not None
    
    def test_documento_tipo_personalizado(self):
        """Test documento con tipo personalizado."""
        documento = DocumentoFactory(tipo='Carta de Recomendación')
        assert documento.tipo == 'Carta de Recomendación'


@pytest.mark.django_db
class TestDocumentoQuerysets:
    """Tests para querysets de documentos."""
    
    def test_filter_documentos_validos(self):
        """Test filtrar documentos válidos."""
        DocumentoValidoFactory.create_batch(3)
        DocumentoInvalidoFactory.create_batch(2)
        
        documentos_validos = Documento.objects.filter(valido=True)
        assert documentos_validos.count() >= 3
    
    def test_filter_documentos_por_tipo(self):
        """Test filtrar documentos por tipo."""
        DocumentoFactory.create_batch(2, tipo='CV')
        DocumentoFactory.create_batch(3, tipo='Certificado')
        
        cvs = Documento.objects.filter(tipo='CV')
        certificados = Documento.objects.filter(tipo='Certificado')
        
        assert cvs.count() >= 2
        assert certificados.count() >= 3
    
    def test_ordenamiento_por_fecha(self):
        """Test ordenamiento por fecha de creación."""
        doc1 = DocumentoFactory()
        doc2 = DocumentoFactory()
        doc3 = DocumentoFactory()
        
        documentos = Documento.objects.all().order_by('-created_at')
        # Verificar que podemos ordenar por fecha
        assert documentos.count() >= 3
