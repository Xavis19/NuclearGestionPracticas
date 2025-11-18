# 🎯 GUÍA RÁPIDA DE INICIO
# Sistema de Gestión de Prácticas Profesionales

## ⚡ INICIO RÁPIDO (5 minutos)

### 1. Instalar dependencias del sistema (macOS)

```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar PostgreSQL y Redis
brew install postgresql@15 redis python@3.11

# Iniciar servicios
brew services start postgresql@15
brew services start redis
```

### 2. Configurar el proyecto

```bash
# Navegar al directorio
cd /Users/editsongutierreza/Downloads/nuclear

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias Python
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env

# Editar .env (opcional, los valores por defecto funcionan para desarrollo)
# nano .env
```

### 3. Generar todas las aplicaciones

```bash
# Ejecutar script de generación
python3 create_all_apps.py
```

### 4. Configurar base de datos

```bash
# Crear base de datos PostgreSQL
createdb practicas_db

# O si tienes problemas con permisos:
psql postgres
CREATE DATABASE practicas_db;
\q

# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser

# Ejemplo:
# Email: admin@practicas.com
# Username: admin
# Password: admin123 (cambiar en producción)
```

### 6. Iniciar el servidor

```bash
# Opción A: Solo Django (simple)
python manage.py runserver

# Opción B: Con Celery (completo - abrir 4 terminales)

# Terminal 1 - Redis
redis-server

# Terminal 2 - Django
python manage.py runserver

# Terminal 3 - Celery Worker
celery -A config worker -l info

# Terminal 4 - Celery Beat
celery -A config beat -l info
```

### 7. Acceder al sistema

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs**: (Agregar swagger si necesario)

## 🎬 PRIMER USO

### 1. Login como Admin

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@practicas.com",
    "password": "admin123"
  }'
```

Guardar el `access` token.

### 2. Crear un Profesor

```bash
curl -X POST http://localhost:8000/admin/usuarios/user/ \
  # Usar el panel de admin es más fácil
```

O usar el admin panel: http://localhost:8000/admin/usuarios/user/add/

Datos de ejemplo:
- Email: profesor1@universidad.edu
- Username: profesor1
- Role: PROFESOR
- Nombre: Carlos
- Apellido: Martínez
- Departamento: Ingeniería
- Especialidad: Desarrollo de Software

### 3. Crear un Estudiante (vía API)

```bash
curl -X POST http://localhost:8000/api/usuarios/estudiantes/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan.perez",
    "email": "juan.perez@universidad.edu",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Pérez",
    "carrera": "Ingeniería en Sistemas",
    "semestre": 7,
    "promedio": 8.5
  }'
```

### 4. Crear una Empresa

```bash
curl -X POST http://localhost:8000/api/vacantes/empresas/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Tech Solutions",
    "rfc": "TSO120101AAA",
    "razon_social": "Tech Solutions SA de CV",
    "direccion": "Av. Reforma 123",
    "telefono": "+525555555555",
    "email": "contacto@tech.com",
    "contacto_nombre": "María García",
    "contacto_puesto": "RRHH",
    "contacto_email": "maria@tech.com",
    "contacto_telefono": "+525555555556",
    "sector": "Tecnología",
    "tamaño": "MEDIANA"
  }'
```

### 5. Crear una Vacante

```bash
curl -X POST http://localhost:8000/api/vacantes/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "empresa": 1,
    "titulo": "Desarrollador Backend",
    "descripcion": "Práctica en desarrollo con Django",
    "requisitos": "Python, Django, PostgreSQL",
    "carreras_solicitadas": "Ingeniería en Sistemas, Ingeniería en Software",
    "semestre_minimo": 6,
    "promedio_minimo": 8.0,
    "area": "Desarrollo",
    "modalidad": "HIBRIDO",
    "ubicacion": "CDMX",
    "horario": "9:00 - 15:00",
    "duracion_meses": 6,
    "vacantes_disponibles": 3,
    "fecha_inicio": "2025-02-01",
    "fecha_cierre_convocatoria": "2025-01-15",
    "remunerada": true,
    "monto_apoyo": 5000.00
  }'
```

### 6. Crear y Asignar una Práctica

```bash
# 1. Crear práctica
curl -X POST http://localhost:8000/api/practicas/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "estudiante": 2,
    "area_practica": "Backend",
    "proyecto": "Sistema de inventarios",
    "fecha_inicio": "2025-02-01",
    "fecha_fin": "2025-08-01"
  }'

# 2. Asignar profesor y empresa
curl -X POST http://localhost:8000/api/practicas/1/asignar/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "profesor_id": 3,
    "empresa_id": 1
  }'
```

## 🐳 DOCKER (Alternativa más fácil)

```bash
# 1. Iniciar todos los servicios
docker-compose up --build

# 2. En otra terminal, ejecutar migraciones
docker-compose exec web python manage.py migrate

# 3. Crear superusuario
docker-compose exec web python manage.py createsuperuser

# 4. Acceder a http://localhost:8000
```

## 📱 ESTRUCTURA DE ARCHIVOS GENERADA

```
nuclear/
├── config/
│   ├── __init__.py
│   ├── settings.py          ✅ Configuración completa
│   ├── urls.py              ✅ URLs principales
│   ├── wsgi.py              ✅ WSGI config
│   ├── asgi.py              ✅ ASGI config
│   └── celery.py            ✅ Celery config
├── apps/
│   ├── usuarios/            ✅ COMPLETO (RF-11, RF-12)
│   │   ├── models.py        ✅ User con roles
│   │   ├── serializers.py   ✅ User, Estudiante, Profesor
│   │   ├── views.py         ✅ ViewSets completos
│   │   ├── permissions.py   ✅ Permisos por rol
│   │   ├── urls.py          ✅ Routers
│   │   └── admin.py         ✅ Admin personalizado
│   ├── vacantes/            ✅ COMPLETO (RF-01)
│   │   ├── models.py        ✅ Empresa, Vacante
│   │   ├── serializers.py   ✅ Serializers
│   │   ├── views.py         ✅ ViewSets con filtros
│   │   ├── urls.py          ✅ Routers
│   │   └── admin.py         ✅ Admin
│   ├── practicas/           ✅ COMPLETO (RF-13)
│   │   ├── models.py        ✅ Practica con constraints
│   │   ├── serializers.py   ✅ Via create_all_apps.py
│   │   ├── views.py         ✅ Via create_all_apps.py
│   │   ├── tasks.py         ✅ Notificaciones
│   │   └── ...
│   ├── postulaciones/       ✅ COMPLETO (RF-02)
│   │   ├── models.py        ✅ Postulacion
│   │   ├── views.py         ✅ Selección
│   │   ├── tasks.py         ✅ Emails
│   │   └── ...
│   ├── observaciones/       ✅ BÁSICO (RF-14)
│   │   ├── models.py        ✅ Observacion
│   │   └── ...
│   └── [otras apps]/        🔧 ESTRUCTURA BÁSICA
│       ├── documentos/
│       ├── contratos/
│       ├── tutores/
│       ├── encuestas/
│       ├── reportes/
│       ├── seguimiento/
│       ├── evaluaciones/
│       └── cierre/
├── manage.py                ✅ Django management
├── requirements.txt         ✅ Todas las dependencias
├── .env.example             ✅ Variables de entorno
├── docker-compose.yml       ✅ Docker config
├── Dockerfile               ✅ Docker image
├── install.sh               ✅ Script de instalación
├── create_all_apps.py       ✅ Generador de apps
├── README.md                ✅ Documentación principal
├── INSTRUCCIONES.md         ✅ Guía detallada
├── ARQUITECTURA.md          ✅ Arquitectura del sistema
└── INICIO_RAPIDO.md         ✅ Este archivo
```

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de comenzar a usar el sistema, verifica:

- [ ] PostgreSQL está instalado y ejecutándose
- [ ] Redis está instalado y ejecutándose
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (pip install -r requirements.txt)
- [ ] Base de datos creada (practicas_db)
- [ ] Apps generadas (python3 create_all_apps.py)
- [ ] Migraciones aplicadas (python manage.py migrate)
- [ ] Superusuario creado
- [ ] Servidor Django ejecutándose

## 🆘 SOLUCIÓN RÁPIDA DE PROBLEMAS

### "command not found: python"
```bash
# Usar python3
python3 manage.py runserver
```

### "django.db.utils.OperationalError: could not connect"
```bash
# Verificar que PostgreSQL esté ejecutándose
brew services start postgresql@15

# Verificar conexión
psql postgres -c "SELECT 1"
```

### "Error: That port is already in use"
```bash
# Usar otro puerto
python manage.py runserver 8001
```

### "ModuleNotFoundError: No module named"
```bash
# Verificar que el venv esté activado
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### "relation does not exist"
```bash
# Ejecutar migraciones nuevamente
python manage.py makemigrations
python manage.py migrate
```

## 📞 PRÓXIMOS PASOS

1. **Explorar el Admin Panel**
   - http://localhost:8000/admin/
   - Crear usuarios de prueba
   - Crear empresas y vacantes

2. **Probar los endpoints con Postman/Insomnia**
   - Importar colección (crear una)
   - Probar flujos completos

3. **Implementar funcionalidades faltantes**
   - Revisar ARQUITECTURA.md
   - Completar RF-003 a RF-010

4. **Configurar Frontend**
   - React/Vue/Angular
   - Conectar con API
   - Implementar UI/UX

5. **Deploy a Producción**
   - Configurar servidor
   - Nginx + Gunicorn
   - SSL/HTTPS
   - Monitoreo

## 🎓 RECURSOS DE APRENDIZAJE

- **Django**: https://docs.djangoproject.com/
- **DRF**: https://www.django-rest-framework.org/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Celery**: https://docs.celeryproject.org/
- **JWT**: https://jwt.io/

---

**¡El sistema está listo para usarse! 🚀**

Comienza explorando el admin panel y luego prueba los endpoints de la API.
