# Guía Rápida de Testing

## 🚀 Inicio Rápido

```bash
# 1. Ejecutar todas las pruebas
./run_tests.sh

# 2. Ver cobertura
./run_tests.sh coverage
open htmlcov/index.html

# 3. Solo pruebas de usuarios
./run_tests.sh usuarios

# 4. Pruebas rápidas
./run_tests.sh quick
```

## 📝 Comandos Comunes

```bash
# Ejecutar pytest directamente
pytest                              # Todas las pruebas
pytest -v                           # Verbose
pytest -x                           # Parar en primer error
pytest -k "test_crear"              # Solo pruebas con "test_crear" en el nombre
pytest apps/usuarios/tests/         # Solo pruebas de usuarios
pytest -m models                    # Solo pruebas marcadas como "models"
pytest --lf                         # Last Failed (re-ejecutar fallidas)
pytest --ff                         # Failed First

# Con cobertura
pytest --cov=apps --cov-report=html
pytest --cov=apps --cov-report=term-missing

# Más rápido (paralelo)
pip install pytest-xdist
pytest -n auto

# Modo watch
pip install pytest-watch
ptw
```

## ✅ Checklist Antes de Commit

- [ ] `./run_tests.sh` - Todas las pruebas pasan
- [ ] Cobertura > 80%
- [ ] Sin warnings
- [ ] Código formateado (black, isort)

## 📚 Estructura de una Prueba

```python
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.django_db  # Requerido para acceso a DB


class TestMiFeature:
    """Descripción del grupo de pruebas."""
    
    def test_caso_exitoso(self, estudiante_factory):
        """Descripción de lo que se prueba."""
        # Arrange: Preparar
        estudiante = estudiante_factory(semestre=5)
        
        # Act: Ejecutar
        resultado = estudiante.avanzar_semestre()
        
        # Assert: Verificar
        assert resultado.semestre == 6
```

## 🔧 Fixtures Disponibles

```python
# Factories
def test_algo(
    user_factory,           # Usuario genérico
    estudiante_factory,     # Estudiante
    profesor_factory,       # Profesor
    coordinador_factory     # Coordinador
):
    pass

# Clientes autenticados
def test_api(
    api_client,             # Sin autenticar
    authenticated_client,   # Usuario genérico
    estudiante_client,      # Como estudiante
    profesor_client,        # Como profesor
    coordinador_client      # Como coordinador
):
    pass
```

## 🎯 Marcadores

```python
@pytest.mark.slow          # Prueba lenta
@pytest.mark.unit          # Prueba unitaria
@pytest.mark.integration   # Prueba de integración
@pytest.mark.api           # Prueba de API
@pytest.mark.models        # Prueba de modelos
@pytest.mark.views         # Prueba de vistas
```

Ejecutar: `pytest -m models` o `pytest -m "not slow"`

## 📊 Metas de Cobertura

- Mínimo: 70%
- Objetivo: 80%
- Ideal: 90%+

## 🐛 Debugging

```python
# Usar breakpoint() en el código
def test_debug(self):
    estudiante = EstudianteFactory()
    breakpoint()  # Detiene aquí
    assert estudiante.pk

# O con pytest
pytest --pdb  # Entra en debugger al fallar
pytest -s     # Muestra prints
```

## 📖 Ver Documentación Completa

`cat TESTING.md` o abre `TESTING.md` en tu editor.
