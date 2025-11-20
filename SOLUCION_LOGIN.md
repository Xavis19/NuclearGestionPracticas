# 🔐 Solución al Problema de Login

## Problema Identificado

El modelo `User` tiene configurado:
```python
USERNAME_FIELD = 'email'  # Django espera EMAIL para autenticar
```

Pero el formulario de login enviaba el **username**, causando que `authenticate()` fallara.

## Solución Implementada

### 1. Creado Backend Personalizado
**Archivo**: `apps/usuarios/backends.py`

Este backend permite login con **email O username**:
- Busca el usuario por email O username usando `Q(email=username) | Q(username=username)`
- Verifica la contraseña
- Es compatible con Axes (protección anti fuerza bruta)

### 2. Actualizado settings.py
```python
AUTHENTICATION_BACKENDS = [
    'apps.usuarios.backends.EmailOrUsernameModelBackend',  # ← Backend personalizado
    'axes.backends.AxesBackend',
]
```

## Cómo Funciona Ahora

### ✅ Puedes hacer login con:
1. **Username**: `admin` + `admin123`
2. **Email**: `admin@example.com` + `admin123`
3. **Cualquier combinación**: El backend busca por ambos campos

## Usuarios de Prueba

```
Username: admin
Email: admin@example.com
Password: admin123
Role: COORDINADOR

Username: xavis19
Email: yhuesosman@gmail.com
Password: (la que configuraste)
Role: COORDINADOR

Username: Arlemoralez27
Email: arlemoralez27@example.com
Password: (la que configuraste)
Role: PROFESOR
```

## Próximos Pasos

1. ✅ **Reiniciar el servidor Django** para que tome los cambios
2. ✅ **Limpiar bloqueos de Axes**: `python manage.py axes_reset`
3. ✅ **Probar login** en el frontend

## Comandos Útiles

```bash
# Limpiar bloqueos de Axes
python manage.py axes_reset

# Ver intentos de login
python manage.py shell -c "from axes.models import AccessAttempt; print(AccessAttempt.objects.all())"

# Probar autenticación
python manage.py shell -c "from django.contrib.auth import authenticate; from django.test import RequestFactory; factory = RequestFactory(); request = factory.post('/'); user = authenticate(request, username='admin', password='admin123'); print(f'Login exitoso: {user}')"
```

## Archivos Modificados

1. ✅ `apps/usuarios/backends.py` - CREADO
2. ✅ `config/settings.py` - MODIFICADO (AUTHENTICATION_BACKENDS)
