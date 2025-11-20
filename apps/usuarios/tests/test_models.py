"""
Pruebas unitarias para los modelos de usuarios.
"""
import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestUserModel:
    """Pruebas para el modelo User."""
    
    def test_create_user_with_email(self, user_factory):
        """Debe crear un usuario con email válido."""
        user = user_factory(email='test@example.com')
        assert user.email == 'test@example.com'
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
    
    def test_create_user_without_email_raises_error(self):
        """Debe fallar al crear usuario sin email."""
        with pytest.raises(ValueError, match='El usuario debe tener un email'):
            User.objects.create_user(email='', password='testpass123')
    
    def test_email_is_normalized(self):
        """El email debe normalizarse automáticamente (dominio en minúsculas)."""
        user = User.objects.create_user(
            email='test@EXAMPLE.COM',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        # normalize_email solo normaliza el dominio (después de @)
        assert user.email == 'test@example.com'
    
    def test_email_is_unique(self):
        """No se pueden crear dos usuarios con el mismo email."""
        User.objects.create_user(
            email='duplicate@example.com',
            username='user1',
            first_name='User',
            last_name='One',
            password='testpass123'
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email='duplicate@example.com',
                username='user2',
                first_name='User',
                last_name='Two',
                password='testpass123'
            )
    
    def test_username_is_unique(self):
        """No se pueden crear dos usuarios con el mismo username."""
        User.objects.create_user(
            email='user1@example.com',
            username='duplicate',
            first_name='User',
            last_name='One',
            password='testpass123'
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email='user2@example.com',
                username='duplicate',
                first_name='User',
                last_name='Two',
                password='testpass123'
            )
    
    def test_user_str_representation(self, user_factory):
        """La representación en string debe incluir nombre y rol."""
        user = user_factory(
            first_name='Juan',
            last_name='Pérez',
            role=User.ESTUDIANTE
        )
        assert 'Juan Pérez' in str(user)
        assert 'Estudiante' in str(user)
    
    def test_get_full_name(self, user_factory):
        """Debe retornar el nombre completo."""
        user = user_factory(first_name='María', last_name='García')
        assert user.get_full_name() == 'María García'
    
    def test_password_is_hashed(self, user_factory):
        """La contraseña debe almacenarse encriptada."""
        user = user_factory(password='testpass123')
        assert user.password != 'testpass123'
        assert user.check_password('testpass123') is True


class TestEstudianteModel:
    """Pruebas específicas para estudiantes."""
    
    def test_create_estudiante(self, estudiante_factory):
        """Debe crear un estudiante con todos sus campos."""
        estudiante = estudiante_factory(
            matricula='EST12345678',
            carrera='Ingeniería en Sistemas',
            semestre=5,
            promedio=85.50
        )
        assert estudiante.role == User.ESTUDIANTE
        assert estudiante.is_estudiante is True
        assert estudiante.matricula == 'EST12345678'
        assert estudiante.carrera == 'Ingeniería en Sistemas'
        assert estudiante.semestre == 5
        assert estudiante.promedio == 85.50
    
    def test_estudiante_matricula_is_unique(self, estudiante_factory):
        """La matrícula debe ser única."""
        estudiante_factory(matricula='EST00000001')
        with pytest.raises(IntegrityError):
            estudiante_factory(matricula='EST00000001')
    
    def test_estudiante_auto_generates_matricula(self):
        """Si no se proporciona matrícula, debe generarse automáticamente."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            role=User.ESTUDIANTE,
            password='testpass123'
        )
        assert user.matricula is not None
        assert user.matricula.startswith('EST')
    
    def test_estudiante_properties(self, estudiante_factory):
        """Las propiedades de rol deben funcionar correctamente."""
        estudiante = estudiante_factory()
        assert estudiante.is_estudiante is True
        assert estudiante.is_profesor is False
        assert estudiante.is_coordinador is False
    
    def test_estudiante_clears_non_student_fields_on_save(self, estudiante_factory):
        """Al guardar un estudiante, los campos de otros roles deben limpiarse."""
        estudiante = estudiante_factory(
            departamento='Sistemas',
            especialidad='IA'
        )
        estudiante.save()
        estudiante.refresh_from_db()
        assert estudiante.departamento is None
        assert estudiante.especialidad is None


class TestProfesorModel:
    """Pruebas específicas para profesores."""
    
    def test_create_profesor(self, profesor_factory):
        """Debe crear un profesor con todos sus campos."""
        profesor = profesor_factory(
            departamento='Sistemas y Computación',
            especialidad='Desarrollo de Software'
        )
        assert profesor.role == User.PROFESOR
        assert profesor.is_profesor is True
        assert profesor.departamento == 'Sistemas y Computación'
        assert profesor.especialidad == 'Desarrollo de Software'
    
    def test_profesor_properties(self, profesor_factory):
        """Las propiedades de rol deben funcionar correctamente."""
        profesor = profesor_factory()
        assert profesor.is_estudiante is False
        assert profesor.is_profesor is True
        assert profesor.is_coordinador is False
    
    def test_profesor_clears_student_fields_on_save(self, profesor_factory):
        """Al guardar un profesor, los campos de estudiante deben limpiarse."""
        profesor = profesor_factory()
        profesor.matricula = 'EST12345678'
        profesor.carrera = 'Ingeniería'
        profesor.save()
        profesor.refresh_from_db()
        assert profesor.matricula is None
        assert profesor.carrera is None


class TestCoordinadorModel:
    """Pruebas específicas para coordinadores."""
    
    def test_create_coordinador(self, coordinador_factory):
        """Debe crear un coordinador."""
        coordinador = coordinador_factory()
        assert coordinador.role == User.COORDINADOR
        assert coordinador.is_coordinador is True
        assert coordinador.is_staff is True
    
    def test_coordinador_properties(self, coordinador_factory):
        """Las propiedades de rol deben funcionar correctamente."""
        coordinador = coordinador_factory()
        assert coordinador.is_estudiante is False
        assert coordinador.is_profesor is False
        assert coordinador.is_coordinador is True


class TestSuperUserCreation:
    """Pruebas para creación de superusuarios."""
    
    def test_create_superuser(self):
        """Debe crear un superusuario correctamente."""
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            first_name='Admin',
            last_name='User',
            password='adminpass123'
        )
        assert superuser.is_superuser is True
        assert superuser.is_staff is True
        assert superuser.is_active is True
        assert superuser.role == User.COORDINADOR
    
    def test_create_superuser_without_is_staff_raises_error(self):
        """Debe fallar si se intenta crear superuser sin is_staff."""
        with pytest.raises(ValueError, match='El superusuario debe tener is_staff=True'):
            User.objects.create_superuser(
                email='admin@example.com',
                username='admin',
                password='adminpass123',
                is_staff=False
            )
    
    def test_create_superuser_without_is_superuser_raises_error(self):
        """Debe fallar si se intenta crear superuser sin is_superuser."""
        with pytest.raises(ValueError, match='El superusuario debe tener is_superuser=True'):
            User.objects.create_superuser(
                email='admin@example.com',
                username='admin',
                password='adminpass123',
                is_superuser=False
            )


class TestUserQuerysets:
    """Pruebas para consultas de usuarios."""
    
    def test_filter_by_role(self, estudiante_factory, profesor_factory):
        """Debe poder filtrar usuarios por rol."""
        # Limpiar usuarios existentes de pruebas anteriores
        initial_estudiantes = User.objects.filter(role=User.ESTUDIANTE).count()
        initial_profesores = User.objects.filter(role=User.PROFESOR).count()
        
        estudiante_factory.create_batch(3)
        profesor_factory.create_batch(2)
        
        estudiantes = User.objects.filter(role=User.ESTUDIANTE)
        profesores = User.objects.filter(role=User.PROFESOR)
        
        assert estudiantes.count() == initial_estudiantes + 3
        assert profesores.count() == initial_profesores + 2
    
    def test_filter_active_users(self, user_factory):
        """Debe poder filtrar usuarios activos."""
        # Contar usuarios activos existentes
        initial_active = User.objects.filter(is_active=True).count()
        
        user_factory.create_batch(3, is_active=True)
        user_factory.create_batch(2, is_active=False)
        
        active_users = User.objects.filter(is_active=True)
        inactive_users = User.objects.filter(is_active=False)
        
        assert active_users.count() == initial_active + 3
        assert inactive_users.count() == 2
    
    def test_ordering(self, user_factory):
        """Los usuarios deben ordenarse por fecha de creación descendente."""
        users = user_factory.create_batch(5)
        queryset = User.objects.all()
        
        # El primer usuario en el queryset debe ser el último creado
        assert queryset.first().created_at >= queryset.last().created_at
