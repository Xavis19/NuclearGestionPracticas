"""
Configuración global de pytest para el proyecto.
"""
import pytest
from django.conf import settings
from django.test import override_settings
from rest_framework.test import APIClient
from apps.usuarios.factories import (
    UserFactory,
    EstudianteFactory,
    ProfesorFactory,
    CoordinadorFactory,
    SuperUserFactory
)


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Configuración de base de datos para testing."""
    with django_db_blocker.unblock():
        # La configuración de BD ya está manejada por pytest-django
        pass


# Fixtures para factories
@pytest.fixture
def user_factory():
    return UserFactory


@pytest.fixture
def estudiante_factory():
    return EstudianteFactory


@pytest.fixture
def profesor_factory():
    return ProfesorFactory


@pytest.fixture
def coordinador_factory():
    return CoordinadorFactory


@pytest.fixture
def superuser_factory():
    return SuperUserFactory


# Fixtures para clientes API
@pytest.fixture
def api_client():
    """Cliente API para hacer requests en las pruebas."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user_factory):
    """Cliente API autenticado con un usuario básico."""
    user = user_factory()
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client


@pytest.fixture
def coordinador_client(api_client, coordinador_factory):
    """Cliente API autenticado como coordinador."""
    coordinador = coordinador_factory()
    api_client.force_authenticate(user=coordinador)
    api_client.user = coordinador
    return api_client


@pytest.fixture
def profesor_client(api_client, profesor_factory):
    """Cliente API autenticado como profesor."""
    profesor = profesor_factory()
    api_client.force_authenticate(user=profesor)
    api_client.user = profesor
    return api_client


@pytest.fixture
def estudiante_client(api_client, estudiante_factory):
    """Cliente API autenticado como estudiante."""
    estudiante = estudiante_factory()
    api_client.force_authenticate(user=estudiante)
    api_client.user = estudiante
    return api_client


@pytest.fixture(autouse=True)
def disable_axes():
    """Deshabilitar django-axes en pruebas."""
    with override_settings(
        AXES_ENABLED=False,
        AXES_FAILURE_LIMIT=999,
    ):
        yield


@pytest.fixture(autouse=True)
def disable_celery(settings):
    """Ejecutar tareas de Celery de forma síncrona en pruebas."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True


@pytest.fixture
def mock_storage(mocker):
    """Mock para Django storage en pruebas de archivos."""
    return mocker.patch('django.core.files.storage.default_storage.save')
