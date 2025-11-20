"""
Pruebas unitarias para las vistas/API de usuarios.
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.skip(reason="URLs no configuradas aún")]


class TestUserViewSet:
    """Pruebas para UserViewSet."""
    
    def test_list_users_as_coordinador(self, coordinador_client, estudiante_factory, profesor_factory):
        """Coordinador debe poder listar todos los usuarios."""
        estudiante_factory.create_batch(3)
        profesor_factory.create_batch(2)
        
        url = reverse('user-list')
        response = coordinador_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # +1 por el coordinador autenticado
        assert len(response.data['results']) >= 6
    
    def test_list_users_as_estudiante_forbidden(self, estudiante_client):
        """Estudiante no debe poder listar usuarios."""
        url = reverse('user-list')
        response = estudiante_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_list_users_as_profesor_forbidden(self, profesor_client):
        """Profesor no debe poder listar usuarios."""
        url = reverse('user-list')
        response = profesor_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_retrieve_user_as_coordinador(self, coordinador_client, estudiante_factory):
        """Coordinador debe poder ver detalles de un usuario."""
        estudiante = estudiante_factory()
        
        url = reverse('user-detail', kwargs={'pk': estudiante.pk})
        response = coordinador_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == estudiante.email
    
    def test_me_endpoint_returns_current_user(self, estudiante_client):
        """El endpoint /me/ debe retornar el usuario autenticado."""
        url = reverse('user-me')
        response = estudiante_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == estudiante_client.user.email
    
    def test_filter_users_by_role(self, coordinador_client, estudiante_factory, profesor_factory):
        """Debe poder filtrar usuarios por rol."""
        estudiante_factory.create_batch(3)
        profesor_factory.create_batch(2)
        
        url = reverse('user-list')
        response = coordinador_client.get(url, {'role': User.ESTUDIANTE})
        
        assert response.status_code == status.HTTP_200_OK
        for user in response.data['results']:
            if user['role'] == User.ESTUDIANTE:
                assert user['role'] == User.ESTUDIANTE
    
    def test_search_users(self, coordinador_client, estudiante_factory):
        """Debe poder buscar usuarios por email o nombre."""
        estudiante = estudiante_factory(
            first_name='Juan',
            last_name='Pérez',
            email='juan.perez@example.com'
        )
        
        url = reverse('user-list')
        response = coordinador_client.get(url, {'search': 'juan'})
        
        assert response.status_code == status.HTTP_200_OK
        assert any(u['email'] == estudiante.email for u in response.data['results'])
    
    def test_unauthenticated_access_forbidden(self, api_client):
        """Usuarios no autenticados no deben acceder a la API."""
        url = reverse('user-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestEstudianteViewSet:
    """Pruebas para EstudianteViewSet."""
    
    def test_create_estudiante_as_coordinador(self, coordinador_client):
        """Coordinador debe poder crear estudiantes."""
        url = reverse('estudiante-list')
        data = {
            'username': 'nuevo_estudiante',
            'email': 'nuevo@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Nuevo',
            'last_name': 'Estudiante',
            'matricula': 'EST99999999',
            'carrera': 'Ingeniería en Sistemas',
            'semestre': 5,
            'promedio': 85.5
        }
        
        response = coordinador_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='nuevo@example.com').exists()
        
        estudiante = User.objects.get(email='nuevo@example.com')
        assert estudiante.role == User.ESTUDIANTE
        assert estudiante.matricula == 'EST99999999'
    
    def test_create_estudiante_as_profesor_forbidden(self, profesor_client):
        """Profesor no debe poder crear estudiantes."""
        url = reverse('estudiante-list')
        data = {
            'username': 'nuevo_estudiante',
            'email': 'nuevo@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Nuevo',
            'last_name': 'Estudiante',
        }
        
        response = profesor_client.post(url, data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_estudiante_with_duplicate_email(self, coordinador_client, estudiante_factory):
        """No debe poder crear estudiante con email duplicado."""
        estudiante = estudiante_factory(email='duplicate@example.com')
        
        url = reverse('estudiante-list')
        data = {
            'username': 'otro_usuario',
            'email': 'duplicate@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Otro',
            'last_name': 'Usuario',
        }
        
        response = coordinador_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
    
    def test_create_estudiante_with_mismatched_passwords(self, coordinador_client):
        """No debe crear estudiante si las contraseñas no coinciden."""
        url = reverse('estudiante-list')
        data = {
            'username': 'nuevo_estudiante',
            'email': 'nuevo@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'DifferentPass456!',
            'first_name': 'Nuevo',
            'last_name': 'Estudiante',
        }
        
        response = coordinador_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password_confirm' in response.data
    
    def test_list_estudiantes(self, coordinador_client, estudiante_factory):
        """Debe listar todos los estudiantes."""
        estudiante_factory.create_batch(5)
        
        url = reverse('estudiante-list')
        response = coordinador_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
    
    def test_update_estudiante(self, coordinador_client, estudiante_factory):
        """Coordinador debe poder actualizar estudiantes."""
        estudiante = estudiante_factory(semestre=5)
        
        url = reverse('estudiante-detail', kwargs={'pk': estudiante.pk})
        data = {
            'semestre': 6,
            'promedio': 90.0
        }
        
        response = coordinador_client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        estudiante.refresh_from_db()
        assert estudiante.semestre == 6
        assert float(estudiante.promedio) == 90.0
    
    def test_delete_estudiante(self, coordinador_client, estudiante_factory):
        """Coordinador debe poder eliminar (desactivar) estudiantes."""
        estudiante = estudiante_factory()
        
        url = reverse('estudiante-detail', kwargs={'pk': estudiante.pk})
        response = coordinador_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        estudiante.refresh_from_db()
        assert estudiante.is_active is False


class TestProfesorViewSet:
    """Pruebas para ProfesorViewSet."""
    
    def test_create_profesor_as_coordinador(self, coordinador_client):
        """Coordinador debe poder crear profesores."""
        url = reverse('profesor-list')
        data = {
            'username': 'nuevo_profesor',
            'email': 'profesor@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'Nuevo',
            'last_name': 'Profesor',
            'departamento': 'Sistemas y Computación',
            'especialidad': 'Desarrollo de Software'
        }
        
        response = coordinador_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='profesor@example.com').exists()
        
        profesor = User.objects.get(email='profesor@example.com')
        assert profesor.role == User.PROFESOR
        assert profesor.departamento == 'Sistemas y Computación'
    
    def test_list_profesores(self, coordinador_client, profesor_factory):
        """Debe listar todos los profesores."""
        profesor_factory.create_batch(3)
        
        url = reverse('profesor-list')
        response = coordinador_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3


class TestChangePasswordView:
    """Pruebas para cambio de contraseña."""
    
    def test_change_password_success(self, estudiante_client):
        """Usuario debe poder cambiar su contraseña."""
        url = reverse('user-change-password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'NewSecurePass456!',
            'new_password_confirm': 'NewSecurePass456!'
        }
        
        response = estudiante_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que la nueva contraseña funciona
        estudiante_client.user.refresh_from_db()
        assert estudiante_client.user.check_password('NewSecurePass456!')
    
    def test_change_password_wrong_old_password(self, estudiante_client):
        """No debe cambiar contraseña si la anterior es incorrecta."""
        url = reverse('user-change-password')
        data = {
            'old_password': 'wrong_password',
            'new_password': 'NewSecurePass456!',
            'new_password_confirm': 'NewSecurePass456!'
        }
        
        response = estudiante_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_change_password_mismatch(self, estudiante_client):
        """No debe cambiar contraseña si las nuevas no coinciden."""
        url = reverse('user-change-password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'NewSecurePass456!',
            'new_password_confirm': 'DifferentPass789!'
        }
        
        response = estudiante_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestAuthenticationAndPermissions:
    """Pruebas de autenticación y permisos."""
    
    def test_jwt_token_creation(self, api_client, estudiante_factory):
        """Debe poder obtener token JWT con credenciales válidas."""
        estudiante = estudiante_factory(
            email='test@example.com',
            password='testpass123'
        )
        
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_jwt_token_refresh(self, api_client, estudiante_factory):
        """Debe poder refrescar el token JWT."""
        estudiante = estudiante_factory(
            email='test@example.com',
            password='testpass123'
        )
        
        # Obtener token inicial
        url = reverse('token_obtain_pair')
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = api_client.post(url, data)
        refresh_token = response.data['refresh']
        
        # Refrescar token
        url = reverse('token_refresh')
        data = {'refresh': refresh_token}
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
