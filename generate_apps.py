"""
Script para crear automáticamente todas las apps del proyecto.
Este script genera la estructura básica de todas las aplicaciones.
"""

import os
import sys

# Definición de las apps y sus componentes
APPS = {
    'practicas': {
        'description': 'RF-013: Asignación de Profesor y Empresa',
        'models': ['Practica'],
    },
    'postulaciones': {
        'description': 'RF-002: Selección de Estudiantes',
        'models': ['Postulacion'],
    },
    'documentos': {
        'description': 'RF-003: Documentación',
        'models': ['Documento', 'TipoDocumento'],
    },
    'contratos': {
        'description': 'RF-004: Contratos/Convenios',
        'models': ['Contrato', 'PlantillaContrato'],
    },
    'tutores': {
        'description': 'RF-005: Asignación de Tutores',
        'models': ['TutorEmpresa', 'AsignacionTutor'],
    },
    'encuestas': {
        'description': 'RF-006: Satisfacción Estudiantes',
        'models': ['EncuestaSatisfaccion', 'PreguntaEncuesta', 'RespuestaEncuesta'],
    },
    'reportes': {
        'description': 'RF-007: Reportes de Gestión',
        'models': ['Reporte', 'ReporteGenerado'],
    },
    'seguimiento': {
        'description': 'RF-008: Seguimiento Semanal',
        'models': ['ReporteSemanal', 'Alerta'],
    },
    'evaluaciones': {
        'description': 'RF-009: Evaluaciones de Tutores',
        'models': ['Evaluacion', 'Rubrica', 'CriterioEvaluacion'],
    },
    'cierre': {
        'description': 'RF-010: Cierre de Prácticas',
        'models': ['ChecklistCierre', 'ActaFinal'],
    },
    'observaciones': {
        'description': 'RF-014: Observaciones del Profesor',
        'models': ['Observacion'],
    },
}

def create_app_structure(app_name, config):
    """Crear estructura básica de una app."""
    base_path = f"apps/{app_name}"
    
    # Crear directorio de la app
    os.makedirs(base_path, exist_ok=True)
    
    # Crear archivos básicos
    files = {
        '__init__.py': '',
        'apps.py': generate_apps_py(app_name),
        'models.py': generate_models_py(app_name, config),
        'serializers.py': generate_serializers_py(app_name),
        'views.py': generate_views_py(app_name),
        'urls.py': generate_urls_py(app_name),
        'admin.py': generate_admin_py(app_name),
        'tasks.py': generate_tasks_py(app_name),
        'tests.py': generate_tests_py(app_name),
    }
    
    for filename, content in files.items():
        filepath = os.path.join(base_path, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(content)
    
    print(f"✓ App '{app_name}' creada exitosamente")


def generate_apps_py(app_name):
    class_name = app_name.capitalize() + 'Config'
    return f'''from django.apps import AppConfig


class {class_name}(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
    verbose_name = '{app_name.capitalize()}'
'''


def generate_models_py(app_name, config):
    return f'''"""
Modelos para la app de {app_name}.
{config['description']}
"""

from django.db import models
from apps.usuarios.models import User

# TODO: Implementar modelos: {', '.join(config['models'])}

class Meta:
    app_label = '{app_name}'
'''


def generate_serializers_py(app_name):
    return f'''"""
Serializers para la app de {app_name}.
"""

from rest_framework import serializers

# TODO: Implementar serializers
'''


def generate_views_py(app_name):
    return f'''"""
Views para la app de {app_name}.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# TODO: Implementar views
'''


def generate_urls_py(app_name):
    return f'''"""
URLs para la app de {app_name}.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# TODO: Registrar routers

app_name = '{app_name}'

urlpatterns = [
    path('', include(router.urls)),
]
'''


def generate_admin_py(app_name):
    return f'''"""
Admin para la app de {app_name}.
"""

from django.contrib import admin

# TODO: Registrar modelos en admin
'''


def generate_tasks_py(app_name):
    return f'''"""
Tareas Celery para la app de {app_name}.
"""

from celery import shared_task

# TODO: Implementar tareas
'''


def generate_tests_py(app_name):
    return f'''"""
Tests para la app de {app_name}.
"""

from django.test import TestCase

# TODO: Implementar tests
'''


if __name__ == '__main__':
    print("Generando estructura de apps...")
    print("=" * 50)
    
    for app_name, config in APPS.items():
        create_app_structure(app_name, config)
    
    print("=" * 50)
    print(f"✓ {len(APPS)} apps generadas correctamente")
    print("\nPróximos pasos:")
    print("1. Implementar los modelos en cada app")
    print("2. Ejecutar: python manage.py makemigrations")
    print("3. Ejecutar: python manage.py migrate")
    print("4. Implementar serializers, views y tests")
