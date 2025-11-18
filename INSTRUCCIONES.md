# INSTRUCCIONES DE INSTALACIÓN Y USO
# Sistema de Gestión de Prácticas Profesionales

## 📦 ESTADO DEL PROYECTO

### ✅ Implementado (Completo)

#### RF-011: Autenticación y Roles
- ✅ Modelo de Usuario personalizado con roles (COORDINADOR, PROFESOR, ESTUDIANTE)
- ✅ Autenticación JWT con SimpleJWT
- ✅ Permisos personalizados por rol
- ✅ Protección contra fuerza bruta (Django Axes)
- ✅ CORS configurado
- ✅ Endpoints:
  - POST /api/auth/login/
  - POST /api/auth/refresh/
  - POST /api/auth/verify/
  - GET /api/usuarios/users/me/
  - POST /api/usuarios/users/change_password/

#### RF-012: Registro de Estudiantes
- ✅ Endpoint para que Coordinadora registre estudiantes
- ✅ Validaciones únicas (email, username, matrícula)
- ✅ Transacciones atómicas
- ✅ Serializers con validación de contraseñas
- ✅ Endpoints:
  - POST /api/usuarios/estudiantes/
  - GET /api/usuarios/estudiantes/
  - GET/PUT/DELETE /api/usuarios/estudiantes/{id}/
  - POST /api/usuarios/estudiantes/{id}/activate/
  - POST /api/usuarios/estudiantes/{id}/deactivate/

#### RF-001: Gestión de Vacantes
- ✅ Modelos Empresa y Vacante
- ✅ ViewSets con filtros avanzados
- ✅ Búsqueda por trigram (opcional en PostgreSQL)
- ✅ Permisos por rol (solo coordinadores crean/editan)
- ✅ Método para verificar requisitos del estudiante
- ✅ Endpoints:
  - GET/POST /api/vacantes/
  - GET/PUT/DELETE /api/vacantes/{id}/
  - POST /api/vacantes/{id}/verificar_requisitos/
  - POST /api/vacantes/{id}/cerrar/
  - POST /api/vacantes/{id}/reabrir/
  - GET /api/vacantes/disponibles/
  - GET/POST /api/vacantes/empresas/
  - POST /api/vacantes/empresas/{id}/verificar/

#### RF-013: Asignación de Profesor y Empresa
- ✅ Modelo Practica con estados
- ✅ Constraint: Un estudiante solo puede tener una práctica activa
- ✅ Validación de cupo del profesor (máx. N estudiantes)
- ✅ Validación de empresa activa
- ✅ Sistema de asignación con notificaciones (preparado para Celery)
- ✅ Endpoints:
  - GET/POST /api/practicas/
  - POST /api/practicas/{id}/asignar/

#### RF-002: Selección de Estudiantes
- ✅ Modelo Postulacion
- ✅ Service layer para selección
- ✅ Validaciones académicas
- ✅ Preparado para notificaciones por email vía Celery
- ✅ Endpoints:
  - GET/POST /api/postulaciones/
  - POST /api/postulaciones/{id}/seleccionar/

#### RF-014: Observaciones del Profesor
- ✅ Modelo Observacion
- ✅ Estructura preparada para permisos específicos
- ✅ Auditoría con timestamps

### 🔧 Implementación Básica (Estructura creada)

Las siguientes funcionalidades tienen la estructura básica creada y requieren
implementación completa de modelos, serializers y views:

- RF-003: Documentación
- RF-004: Contratos/Convenios
- RF-005: Asignación de Tutores
- RF-006: Satisfacción Estudiantes
- RF-007: Reportes de Gestión
- RF-008: Seguimiento Semanal
- RF-009: Evaluaciones de Tutores
- RF-010: Cierre de Prácticas

## 🚀 INSTALACIÓN

### Opción 1: Instalación Local con script automatizado

```bash
# 1. Dar permisos de ejecución al script
chmod +x install.sh

# 2. Ejecutar el script de instalación
./install.sh
```

### Opción 2: Instalación Manual

#### Paso 1: Requisitos previos

- Python 3.11+
- PostgreSQL 15+
- Redis 7+

En macOS:
```bash
brew install postgresql redis
brew services start postgresql
brew services start redis
```

#### Paso 2: Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Paso 3: Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Paso 4: Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

#### Paso 5: Crear base de datos

```bash
createdb practicas_db
```

#### Paso 6: Generar apps adicionales

```bash
python create_all_apps.py
```

#### Paso 7: Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Paso 8: Crear superusuario

```bash
python manage.py createsuperuser
```

#### Paso 9: Recopilar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

### Opción 3: Docker

```bash
# 1. Construir y levantar contenedores
docker-compose up --build

# 2. En otra terminal, ejecutar migraciones
docker-compose exec web python manage.py migrate

# 3. Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

## 🎮 USO DEL SISTEMA

### Iniciar el sistema (Local)

```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Celery Worker
source venv/bin/activate
celery -A config worker -l info

# Terminal 3: Celery Beat
source venv/bin/activate
celery -A config beat -l info

# Terminal 4: Django
source venv/bin/activate
python manage.py runserver
```

### Acceso

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: (Agregar django-rest-swagger si se desea)

## 📖 EJEMPLOS DE USO DE LA API

### 1. Autenticación

#### Login (Obtener JWT)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "coordinador@universidad.edu",
    "password": "tu_password"
  }'
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refrescar Token
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

### 2. Gestión de Estudiantes (RF-012)

#### Registrar Estudiante (Solo Coordinador)
```bash
curl -X POST http://localhost:8000/api/usuarios/estudiantes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan.perez",
    "email": "juan.perez@universidad.edu",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "+525512345678",
    "carrera": "Ingeniería en Sistemas",
    "semestre": 7,
    "promedio": 8.5
  }'
```

#### Listar Estudiantes
```bash
curl -X GET http://localhost:8000/api/usuarios/estudiantes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Filtrar Estudiantes
```bash
# Por carrera
curl -X GET "http://localhost:8000/api/usuarios/estudiantes/?carrera=Ingeniería%20en%20Sistemas" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Por semestre
curl -X GET "http://localhost:8000/api/usuarios/estudiantes/?semestre=7" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Búsqueda
curl -X GET "http://localhost:8000/api/usuarios/estudiantes/?search=Juan" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Gestión de Empresas y Vacantes (RF-001)

#### Crear Empresa (Solo Coordinador)
```bash
curl -X POST http://localhost:8000/api/vacantes/empresas/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Tech Solutions SA",
    "rfc": "TSO120101AAA",
    "razon_social": "Tech Solutions Sociedad Anónima",
    "direccion": "Av. Reforma 123, CDMX",
    "telefono": "+525555555555",
    "email": "contacto@techsolutions.com",
    "sitio_web": "https://techsolutions.com",
    "contacto_nombre": "María García",
    "contacto_puesto": "Gerente de RRHH",
    "contacto_email": "maria.garcia@techsolutions.com",
    "contacto_telefono": "+525555555556",
    "sector": "Tecnología",
    "tamaño": "MEDIANA"
  }'
```

#### Crear Vacante (Solo Coordinador)
```bash
curl -X POST http://localhost:8000/api/vacantes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "empresa": 1,
    "titulo": "Desarrollador Backend Junior",
    "descripcion": "Práctica profesional en desarrollo de aplicaciones web con Django y Python",
    "requisitos": "Conocimientos en Python, Django, bases de datos SQL, Git",
    "carreras_solicitadas": "Ingeniería en Sistemas, Ingeniería en Software, Ciencias de la Computación",
    "semestre_minimo": 6,
    "promedio_minimo": 8.0,
    "area": "Desarrollo de Software",
    "modalidad": "HIBRIDO",
    "ubicacion": "CDMX - Santa Fe",
    "horario": "Lunes a Viernes, 9:00 - 15:00",
    "duracion_meses": 6,
    "vacantes_disponibles": 3,
    "fecha_inicio": "2025-01-15",
    "fecha_cierre_convocatoria": "2024-12-15",
    "remunerada": true,
    "monto_apoyo": 5000.00,
    "beneficios_adicionales": "Seguro médico, vales de despensa, capacitación"
  }'
```

#### Listar Vacantes Disponibles (Estudiantes)
```bash
curl -X GET http://localhost:8000/api/vacantes/disponibles/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Verificar Requisitos para Vacante
```bash
curl -X POST http://localhost:8000/api/vacantes/1/verificar_requisitos/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Asignación de Prácticas (RF-013)

#### Crear Práctica
```bash
curl -X POST http://localhost:8000/api/practicas/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "estudiante": 5,
    "area_practica": "Desarrollo Backend",
    "proyecto": "Sistema de gestión de inventarios",
    "fecha_inicio": "2025-01-15",
    "fecha_fin": "2025-07-15"
  }'
```

#### Asignar Profesor y Empresa (Solo Coordinador)
```bash
curl -X POST http://localhost:8000/api/practicas/1/asignar/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "profesor_id": 3,
    "empresa_id": 1
  }'
```

### 5. Postulaciones (RF-002)

#### Crear Postulación (Estudiante)
```bash
curl -X POST http://localhost:8000/api/postulaciones/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vacante": 1,
    "motivacion": "Estoy muy interesado en esta oportunidad porque..."
  }'
```

#### Seleccionar Estudiante (Coordinador/Empresa)
```bash
curl -X POST http://localhost:8000/api/postulaciones/1/seleccionar/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔐 ROLES Y PERMISOS

### COORDINADOR
- ✅ Crear, editar, eliminar usuarios (estudiantes, profesores)
- ✅ Gestionar empresas
- ✅ Crear y gestionar vacantes
- ✅ Asignar prácticas (profesor + empresa)
- ✅ Ver todas las prácticas
- ✅ Acceso completo al sistema

### PROFESOR
- ✅ Ver sus estudiantes asignados
- ✅ Crear observaciones en prácticas asignadas
- ✅ Ver listado de estudiantes
- ✅ Ver vacantes

### ESTUDIANTE
- ✅ Ver su perfil
- ✅ Ver vacantes disponibles
- ✅ Postularse a vacantes
- ✅ Ver sus prácticas
- ✅ Verificar requisitos para vacantes

## 📝 PRÓXIMOS PASOS

### Para completar el sistema, implementar:

1. **RF-003 (Documentación)**:
   - Modelo Documento con validación MIME
   - Upload de archivos con hash
   - Integración con S3 (producción)

2. **RF-004 (Contratos/Convenios)**:
   - Generación de PDFs con WeasyPrint
   - Plantillas de contratos
   - Sistema de firmas

3. **RF-005 (Tutores)**:
   - Modelo TutorEmpresa
   - Asignación automática
   - Reglas de idoneidad

4. **RF-006 (Encuestas)**:
   - Modelo de encuestas
   - Sistema de recordatorios
   - Análisis de resultados

5. **RF-007 (Reportes)**:
   - KPIs y métricas
   - Generación asíncrona con Celery
   - Exportación CSV/XLSX

6. **RF-008 (Seguimiento Semanal)**:
   - Reportes semanales
   - Recordatorios automáticos (Celery beat)
   - Alertas de riesgo

7. **RF-009 (Evaluaciones)**:
   - Rúbricas de evaluación
   - Cálculo de puntajes
   - Auditoría con django-simple-history

8. **RF-010 (Cierre de Prácticas)**:
   - Checklist de cierre
   - Generación de acta final
   - Validaciones completas

### Tareas de Celery pendientes:
- Implementar envío de emails
- Configurar tareas programadas (beat)
- Recordatorios automáticos

## 🧪 TESTING

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=apps

# Test específico
pytest apps/usuarios/tests.py
```

## 📊 MONITOREO

- Logs: `logs/django.log`
- Admin: `/admin/`
- Sentry (opcional): Configurar SENTRY_DSN en .env

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error de importación de Django
```bash
# Asegúrate de que el entorno virtual esté activado
source venv/bin/activate
pip install -r requirements.txt
```

### Error de base de datos
```bash
# Verificar que PostgreSQL esté ejecutándose
brew services start postgresql

# Verificar conexión
psql -U postgres -d practicas_db
```

### Error de Redis
```bash
# Iniciar Redis
brew services start redis

# O manualmente
redis-server
```

## 📞 SOPORTE

Para dudas o problemas, revisar:
1. README.md
2. Documentación de Django: https://docs.djangoproject.com/
3. Documentación de DRF: https://www.django-rest-framework.org/

---

**Desarrollado con Django 4.2 + DRF + PostgreSQL + Celery + Redis**
