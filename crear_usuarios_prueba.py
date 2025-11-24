"""
Script para crear usuarios de prueba para cada rol del sistema.
Ejecutar con: python crear_usuarios_prueba.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.usuarios.models import User
from apps.vacantes.models import Empresa

def crear_usuarios_prueba():
    print("=== Creando usuarios de prueba ===\n")
    
    # 1. Crear Coordinadora
    coordinadora, created = User.objects.get_or_create(
        username='coordinadora',
        defaults={
            'email': 'coordinadora@nuclear.com',
            'first_name': 'María',
            'last_name': 'González',
            'role': User.COORDINADORA_EMPRESARIAL,
            'is_staff': True,
            'is_active': True,
        }
    )
    if created:
        coordinadora.set_password('nuclear123')
        coordinadora.save()
        print("✅ Coordinadora creada")
        print(f"   Usuario: coordinadora")
        print(f"   Password: nuclear123\n")
    else:
        print("⚠️  Coordinadora ya existe\n")
    
    # 2. Crear Empresa
    empresa, created = Empresa.objects.get_or_create(
        rfc='20123456789',
        defaults={
            'nombre': 'Tech Solutions S.A.C.',
            'razon_social': 'Tech Solutions S.A.C.',
            'direccion': 'Av. Principal 123, Lima',
            'telefono': '987654321',
            'email': 'contacto@techsolutions.com',
            'activa': True,
        }
    )
    if created:
        print("✅ Empresa creada: Tech Solutions S.A.C.\n")
    else:
        print("⚠️  Empresa ya existe\n")
    
    # 3. Crear Tutor Empresarial
    tutor, created = User.objects.get_or_create(
        username='tutor',
        defaults={
            'email': 'tutor@techsolutions.com',
            'first_name': 'Carlos',
            'last_name': 'Ramírez',
            'role': User.TUTOR_EMPRESARIAL,
            'empresa': empresa,
            'is_active': True,
        }
    )
    if created:
        tutor.set_password('nuclear123')
        tutor.save()
        print("✅ Tutor Empresarial creado")
        print(f"   Usuario: tutor")
        print(f"   Password: nuclear123")
        print(f"   Empresa: {empresa.nombre}\n")
    else:
        print("⚠️  Tutor ya existe\n")
    
    # 4. Crear Docente Asesor
    docente, created = User.objects.get_or_create(
        username='docente',
        defaults={
            'email': 'docente@universidad.edu.pe',
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'role': User.DOCENTE_ASESOR,
            'is_active': True,
        }
    )
    if created:
        docente.set_password('nuclear123')
        docente.save()
        print("✅ Docente Asesor creado")
        print(f"   Usuario: docente")
        print(f"   Password: nuclear123\n")
    else:
        print("⚠️  Docente ya existe\n")
    
    # 5. Crear Estudiante
    estudiante, created = User.objects.get_or_create(
        username='estudiante',
        defaults={
            'email': 'estudiante@universidad.edu.pe',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'role': User.ESTUDIANTE,
            'carrera': 'Ingeniería de Sistemas',
            'is_active': True,
        }
    )
    if created:
        estudiante.set_password('nuclear123')
        estudiante.save()
        print("✅ Estudiante creado")
        print(f"   Usuario: estudiante")
        print(f"   Password: nuclear123\n")
    else:
        print("⚠️  Estudiante ya existe\n")
    
    print("=== Resumen de usuarios ===")
    print("Todos los usuarios tienen password: nuclear123\n")
    print("Roles creados:")
    print(f"  - Coordinadora: coordinadora@nuclear.com")
    print(f"  - Tutor: tutor@techsolutions.com")
    print(f"  - Docente: docente@universidad.edu.pe")
    print(f"  - Estudiante: estudiante@universidad.edu.pe")
    print("\n¡Listo! Ahora puedes iniciar sesión con cualquiera de estos usuarios.")

if __name__ == '__main__':
    crear_usuarios_prueba()
