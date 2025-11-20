# 🧪 Sistema de Pruebas Unitarias Automatizadas

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Instalación](#instalación)
- [Estructura de Pruebas](#estructura-de-pruebas)
- [Ejecutar Pruebas](#ejecutar-pruebas)
- [Cobertura de Código](#cobertura-de-código)
- [Escribir Nuevas Pruebas](#escribir-nuevas-pruebas)
- [Mejores Prácticas](#mejores-prácticas)
- [Troubleshooting](#troubleshooting)

## 🎯 Descripción General

Este proyecto utiliza **pytest** como framework de pruebas unitarias, junto con:

- **pytest-django**: Integración con Django
- **pytest-cov**: Reportes de cobertura de código
- **factory-boy**: Generación de datos de prueba
- **faker**: Datos realistas falsos
- **pytest-watch**: Ejecución automática al detectar cambios (opcional)

### ✨ Características

- ✅ Pruebas automatizadas completas
- 📊 Reportes de cobertura de código
- 🏭 Factories para generación de datos
- 🔄 Fixtures reutilizables
- 🚀 Ejecución rápida con base de datos en memoria
- 📝 Marcadores personalizados para organizar pruebas

## 📦 Instalación

Las dependencias de testing ya están incluidas en `requirements.txt`:

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias (si no lo has hecho)
pip install -r requirements.txt

# Verificar instalación
pytest --version
```

### Dependencias Opcionales

```bash
# Para modo watch (ejecución continua)
pip install pytest-watch

# Para pruebas paralelas (más rápidas)
pip install pytest-xdist
```

## 📁 Estructura de Pruebas

```
nuclear/
├── conftest.py                 # Configuración global de pytest
├── pytest.ini                  # Configuración de pytest
├── .coveragerc                 # Configuración de cobertura
├── run_tests.sh               # Script principal de ejecución
├── factories.py               # Factories globales
│
├── apps/
│   └── usuarios/
│       ├── factories.py       # Factories específicas de usuarios
│       └── tests/
│           ├── __init__.py
│           ├── test_models.py      # Pruebas de modelos
│           ├── test_views.py       # Pruebas de vistas/API
│           ├── test_serializers.py # Pruebas de serializers
│           └── test_permissions.py # Pruebas de permisos
│
└── htmlcov/                   # Reporte HTML de cobertura (generado)
```

## 🚀 Ejecutar Pruebas

### Uso Básico del Script

```bash
# Ejecutar TODAS las pruebas con cobertura
./run_tests.sh

# o especificar explícitamente
./run_tests.sh all
```

### Opciones Disponibles

```bash
# Pruebas por módulo
./run_tests.sh usuarios     # Solo pruebas de usuarios

# Pruebas por tipo
./run_tests.sh models       # Solo modelos
./run_tests.sh views        # Solo vistas/API
./run_tests.sh api          # Solo endpoints API

# Ejecución rápida (excluye pruebas lentas)
./run_tests.sh quick

# Reporte detallado de cobertura
./run_tests.sh coverage

# Modo watch (ejecuta al detectar cambios)
./run_tests.sh watch

# Ver ayuda
./run_tests.sh help
```

### Usando pytest Directamente

```bash
# Todas las pruebas
pytest

# Pruebas específicas
pytest apps/usuarios/tests/test_models.py
pytest apps/usuarios/tests/test_views.py::TestUserViewSet

# Con verbosidad
pytest -v

# Solo una prueba específica
pytest apps/usuarios/tests/test_models.py::TestUserModel::test_create_user_with_email

# Pruebas marcadas
pytest -m models          # Solo pruebas de modelos
pytest -m "not slow"      # Excluir pruebas lentas

# Modo parallel (más rápido)
pytest -n auto

# Detener en primer error
pytest -x

# Mostrar print statements
pytest -s
```

## 📊 Cobertura de Código

### Ver Reporte en Terminal

```bash
pytest --cov=apps --cov=config --cov-report=term-missing
```

### Generar Reporte HTML

```bash
./run_tests.sh coverage

# Abrir reporte
open htmlcov/index.html
```

### Configuración de Cobertura

El archivo `.coveragerc` controla qué se incluye/excluye:

```ini
[run]
source = apps, config
omit = 
    */migrations/*
    */tests/*
    */__pycache__/*
```

## ✍️ Escribir Nuevas Pruebas

### 1. Crear Archivo de Prueba

```python
# apps/mi_app/tests/test_models.py
"""
Pruebas para modelos de mi_app.
"""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

# Marca todas las pruebas como requiriendo DB
pytestmark = pytest.mark.django_db


class TestMiModelo:
    """Pruebas para MiModelo."""
    
    def test_crear_instancia(self):
        """Debe crear una instancia correctamente."""
        # Arrange (Preparar)
        datos = {'campo': 'valor'}
        
        # Act (Actuar)
        instancia = MiModelo.objects.create(**datos)
        
        # Assert (Verificar)
        assert instancia.campo == 'valor'
        assert instancia.pk is not None
```

### 2. Usar Factories

```python
from apps.usuarios.factories import EstudianteFactory

def test_con_factory(self):
    """Usar factory para crear datos de prueba."""
    # Crear un estudiante
    estudiante = EstudianteFactory()
    
    # Crear con valores específicos
    estudiante = EstudianteFactory(
        email='especifico@example.com',
        semestre=5
    )
    
    # Crear múltiples
    estudiantes = EstudianteFactory.create_batch(5)
```

### 3. Usar Fixtures

```python
def test_con_fixture(self, estudiante_client):
    """Usar cliente autenticado de fixture."""
    url = reverse('mi-endpoint')
    response = estudiante_client.get(url)
    
    assert response.status_code == 200
```

### 4. Marcadores Personalizados

```python
@pytest.mark.slow
def test_operacion_lenta(self):
    """Esta prueba es lenta."""
    # Código de prueba lenta
    pass

@pytest.mark.api
def test_endpoint(self):
    """Prueba de endpoint API."""
    pass
```

## 🎯 Mejores Prácticas

### Nomenclatura

```python
# ✅ BIEN
def test_usuario_puede_cambiar_contrasena(self):
    """Descripción clara de qué se prueba."""
    pass

# ❌ MAL
def test_1(self):
    pass
```

### Estructura AAA

```python
def test_ejemplo(self):
    """Usar patrón Arrange-Act-Assert."""
    
    # Arrange: Preparar datos
    usuario = UserFactory()
    datos = {'campo': 'valor'}
    
    # Act: Ejecutar acción
    resultado = usuario.hacer_algo(datos)
    
    # Assert: Verificar resultado
    assert resultado.exito is True
```

### Un Concepto por Prueba

```python
# ✅ BIEN: Una prueba, un concepto
def test_usuario_puede_login(self):
    """Probar solo login."""
    pass

def test_usuario_puede_logout(self):
    """Probar solo logout."""
    pass

# ❌ MAL: Múltiples conceptos
def test_usuario_login_y_logout_y_cambio_password(self):
    """Demasiadas cosas en una prueba."""
    pass
```

### Independencia

```python
# ✅ BIEN: Cada prueba es independiente
@pytest.mark.django_db
def test_independiente(self):
    """Crear sus propios datos."""
    usuario = UserFactory()
    # usar usuario...

# ❌ MAL: Depender de orden de ejecución
global_usuario = None

def test_crear_usuario(self):
    global global_usuario
    global_usuario = UserFactory()

def test_usar_usuario(self):
    # Depende de test_crear_usuario
    assert global_usuario is not None
```

### Uso de Fixtures

```python
# Crear fixtures reutilizables en conftest.py
@pytest.fixture
def usuario_con_practica(estudiante_factory):
    """Fixture compuesta."""
    estudiante = estudiante_factory()
    practica = Practica.objects.create(
        estudiante=estudiante,
        estado='ACTIVA'
    )
    return estudiante
```

## 🔧 Troubleshooting

### Problema: Base de datos no se limpia entre pruebas

```bash
# Usar --reuse-db con cuidado
pytest --create-db  # Recrear DB

# O limpiar manualmente
rm db.sqlite3
pytest
```

### Problema: Imports no funcionan

```python
# Asegurarse de tener __init__.py en carpetas tests/
# apps/usuarios/tests/__init__.py
```

### Problema: Fixtures no encontrados

```python
# Verificar que conftest.py esté en el lugar correcto
# Debe estar en la raíz o en el directorio padre de tests
```

### Problema: Pruebas muy lentas

```bash
# Usar --reuse-db
pytest --reuse-db

# Usar --nomigrations
pytest --nomigrations

# Ejecutar en paralelo
pytest -n auto

# Ejecutar solo pruebas rápidas
pytest -m "not slow"
```

### Problema: Errores de permisos

```bash
# Asegurar que el script tenga permisos
chmod +x run_tests.sh
```

## 📈 Objetivos de Cobertura

- **Mínimo aceptable**: 70%
- **Objetivo**: 80%
- **Ideal**: 90%+

### Ver Archivos con Baja Cobertura

```bash
pytest --cov=apps --cov-report=term-missing:skip-covered
```

## 🔄 Integración Continua (CI/CD)

Para GitHub Actions, GitLab CI, etc:

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest --cov=apps --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## 📚 Recursos Adicionales

- [Documentación de pytest](https://docs.pytest.org/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [factory-boy](https://factoryboy.readthedocs.io/)
- [Cobertura de código](https://coverage.readthedocs.io/)

## 🤝 Contribuir

Al agregar nuevas funcionalidades:

1. ✅ Escribir pruebas PRIMERO (TDD)
2. ✅ Mantener cobertura > 80%
3. ✅ Todas las pruebas deben pasar
4. ✅ Seguir las mejores prácticas

---

**¡Feliz Testing! 🎉**
