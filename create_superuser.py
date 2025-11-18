#!/usr/bin/env python
"""
Script para crear un superusuario de forma programática
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.usuarios.models import User

def create_superuser():
    """Crear superusuario coordinador"""
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'  # Cambiar en producción
    
    if User.objects.filter(username=username).exists():
        print(f'❌ El usuario "{username}" ya existe')
        user = User.objects.get(username=username)
        print(f'✓ Usuario: {user.username}')
        print(f'✓ Email: {user.email}')
        print(f'✓ Rol: {user.role}')
        return
    
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Admin',
        last_name='Sistema',
        phone='+525512345678'
    )
    
    print('✅ Superusuario creado exitosamente!')
    print(f'✓ Usuario: {user.username}')
    print(f'✓ Email: {user.email}')
    print(f'✓ Contraseña: {password}')
    print(f'✓ Rol: {user.role}')
    print(f'✓ Es staff: {user.is_staff}')
    print(f'✓ Es superuser: {user.is_superuser}')
    print('')
    print('Puedes acceder al admin en: http://localhost:8000/admin/')

if __name__ == '__main__':
    create_superuser()
