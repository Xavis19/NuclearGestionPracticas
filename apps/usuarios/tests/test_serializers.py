"""
Pruebas unitarias para los serializers de usuarios.
"""
import pytest
from django.contrib.auth import get_user_model
from apps.usuarios.serializers import (
    UserSerializer,
    EstudianteSerializer,
    ProfesorSerializer,
    CoordinadorSerializer,
    ChangePasswordSerializer
)

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestUserSerializer:
    """Pruebas para UserSerializer."""
    
    def test_serialize_user(self, user_factory):
        """Debe serializar un usuario correctamente."""
        user = user_factory(
            email='test@example.com',
            first_name='Juan',
            last_name='Pérez'
        )
        
        serializer = UserSerializer(user)
        data = serializer.data
        
        assert data['email'] == 'test@example.com'
        assert data['first_name'] == 'Juan'
        assert data['last_name'] == 'Pérez'
        assert data['full_name'] == 'Juan Pérez'
        assert 'password' not in data
    
    def test_read_only_fields(self, user_factory):
        """Los campos de solo lectura no deben modificarse."""
        user = user_factory()
        original_id = user.id
        original_created = user.created_at
        
        serializer = UserSerializer(user, data={
            'id': 999,
            'created_at': '2020-01-01T00:00:00Z',
            'first_name': 'Nuevo'
        }, partial=True)
        
        assert serializer.is_valid()
        serializer.save()
        user.refresh_from_db()
        
        assert user.id == original_id
        assert user.created_at == original_created
        assert user.first_name == 'Nuevo'


class TestEstudianteSerializer:
    """Pruebas para EstudianteSerializer."""
    
    def test_create_estudiante_valid_data(self):
        """Debe crear un estudiante con datos válidos."""
        data = {
            'username': 'estudiante01',
            'email': 'estudiante@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Carlos',
            'last_name': 'González',
            'matricula': 'EST12345678',
            'carrera': 'Ingeniería en Sistemas',
            'semestre': 5,
            'promedio': 85.5
        }
        
        serializer = EstudianteSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        
        estudiante = serializer.save()
        assert estudiante.role == User.ESTUDIANTE
        assert estudiante.email == 'estudiante@example.com'
        assert estudiante.matricula == 'EST12345678'
        assert estudiante.check_password('SecurePass123!')
    
    def test_password_mismatch_validation(self):
        """Debe fallar si las contraseñas no coinciden."""
        data = {
            'username': 'estudiante01',
            'email': 'estudiante@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'DifferentPass456!',
            'first_name': 'Carlos',
            'last_name': 'González',
        }
        
        serializer = EstudianteSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password_confirm' in serializer.errors or 'non_field_errors' in serializer.errors
    
    def test_duplicate_email_validation(self, estudiante_factory):
        """Debe fallar si el email ya existe."""
        estudiante_factory(email='duplicate@example.com')
        
        data = {
            'username': 'estudiante02',
            'email': 'duplicate@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Carlos',
            'last_name': 'González',
        }
        
        serializer = EstudianteSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors
    
    def test_duplicate_username_validation(self, estudiante_factory):
        """Debe fallar si el username ya existe."""
        estudiante_factory(username='duplicate')
        
        data = {
            'username': 'duplicate',
            'email': 'new@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Carlos',
            'last_name': 'González',
        }
        
        serializer = EstudianteSerializer(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors
    
    def test_duplicate_matricula_validation(self, estudiante_factory):
        """Debe fallar si la matrícula ya existe."""
        estudiante_factory(matricula='EST00000001')
        
        data = {
            'username': 'estudiante02',
            'email': 'new@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Carlos',
            'last_name': 'González',
            'matricula': 'EST00000001'
        }
        
        serializer = EstudianteSerializer(data=data)
        assert not serializer.is_valid()
        assert 'matricula' in serializer.errors
    
    def test_update_estudiante(self, estudiante_factory):
        """Debe actualizar un estudiante correctamente."""
        estudiante = estudiante_factory(semestre=5, promedio=80.0)
        
        data = {
            'semestre': 6,
            'promedio': 85.5
        }
        
        serializer = EstudianteSerializer(estudiante, data=data, partial=True)
        assert serializer.is_valid()
        
        updated = serializer.save()
        assert updated.semestre == 6
        assert float(updated.promedio) == 85.5
    
    def test_password_not_in_serialized_data(self, estudiante_factory):
        """La contraseña no debe aparecer en los datos serializados."""
        estudiante = estudiante_factory()
        
        serializer = EstudianteSerializer(estudiante)
        data = serializer.data
        
        assert 'password' not in data
        assert 'password_confirm' not in data


class TestProfesorSerializer:
    """Pruebas para ProfesorSerializer."""
    
    def test_create_profesor_valid_data(self):
        """Debe crear un profesor con datos válidos."""
        data = {
            'username': 'profesor01',
            'email': 'profesor@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'María',
            'last_name': 'López',
            'departamento': 'Sistemas y Computación',
            'especialidad': 'Base de Datos'
        }
        
        serializer = ProfesorSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        
        profesor = serializer.save()
        assert profesor.role == User.PROFESOR
        assert profesor.email == 'profesor@example.com'
        assert profesor.departamento == 'Sistemas y Computación'
        assert profesor.especialidad == 'Base de Datos'
    
    def test_update_profesor(self, profesor_factory):
        """Debe actualizar un profesor correctamente."""
        profesor = profesor_factory(departamento='Sistemas')
        
        data = {
            'departamento': 'Ciencias Básicas',
            'especialidad': 'Matemáticas'
        }
        
        serializer = ProfesorSerializer(profesor, data=data, partial=True)
        assert serializer.is_valid()
        
        updated = serializer.save()
        assert updated.departamento == 'Ciencias Básicas'
        assert updated.especialidad == 'Matemáticas'


class TestCoordinadorSerializer:
    """Pruebas para CoordinadorSerializer."""
    
    def test_create_coordinador_valid_data(self):
        """Debe crear un coordinador con datos válidos."""
        data = {
            'username': 'coordinador01',
            'email': 'coordinador@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Ana',
            'last_name': 'Martínez',
        }
        
        serializer = CoordinadorSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        
        coordinador = serializer.save()
        assert coordinador.role == User.COORDINADOR
        assert coordinador.email == 'coordinador@example.com'
        assert coordinador.is_staff is True


class TestChangePasswordSerializer:
    """Pruebas para ChangePasswordSerializer."""
    
    def test_validate_passwords_match(self, user_factory):
        """Debe validar que las nuevas contraseñas coincidan."""
        user = user_factory(password='oldpass123')
        
        data = {
            'old_password': 'oldpass123',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        }
        
        serializer = ChangePasswordSerializer(data=data, context={'request': type('obj', (object,), {'user': user})()})
        assert serializer.is_valid()
    
    def test_validate_passwords_mismatch(self, user_factory):
        """Debe fallar si las nuevas contraseñas no coinciden."""
        user = user_factory(password='oldpass123')
        
        data = {
            'old_password': 'oldpass123',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'DifferentPass456!'
        }
        
        serializer = ChangePasswordSerializer(data=data, context={'request': type('obj', (object,), {'user': user})()})
        assert not serializer.is_valid()
    
    def test_validate_old_password_correct(self, user_factory):
        """Debe validar que la contraseña anterior sea correcta."""
        user = user_factory(password='oldpass123')
        
        data = {
            'old_password': 'oldpass123',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        }
        
        serializer = ChangePasswordSerializer(data=data, context={'request': type('obj', (object,), {'user': user})()})
        assert serializer.is_valid()
    
    def test_validate_old_password_incorrect(self, user_factory):
        """Debe fallar si la contraseña anterior es incorrecta."""
        user = user_factory(password='oldpass123')
        
        data = {
            'old_password': 'wrongpass',
            'new_password': 'NewPass123!',
            'new_password_confirm': 'NewPass123!'
        }
        
        serializer = ChangePasswordSerializer(data=data, context={'request': type('obj', (object,), {'user': user})()})
        assert not serializer.is_valid()


class TestSerializerFieldValidation:
    """Pruebas de validación de campos."""
    
    def test_email_format_validation(self):
        """Debe validar el formato del email."""
        data = {
            'username': 'test',
            'email': 'invalid-email',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Test',
            'last_name': 'User',
        }
        
        serializer = EstudianteSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors
    
    def test_required_fields_validation(self):
        """Debe validar campos requeridos."""
        data = {
            'username': 'test',
            # Falta email, password, nombres
        }
        
        serializer = EstudianteSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors
        assert 'first_name' in serializer.errors
        assert 'last_name' in serializer.errors
