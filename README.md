# 🎓 Sistema de Gestión de Prácticas Profesionales

Sistema completo de gestión de prácticas profesionales desarrollado con Django, Django REST Framework y PostgreSQL.

---

## 📚 NAVEGACIÓN RÁPIDA

### 🚀 Para Comenzar
- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Guía de 5 minutos para instalar y ejecutar
- **[INSTRUCCIONES.md](INSTRUCCIONES.md)** - Guía detallada de instalación, configuración y ejemplos de uso

### 📖 Documentación Técnica
- **[ARQUITECTURA.md](ARQUITECTURA.md)** - Arquitectura completa del sistema, modelos, flujos y endpoints
- **[RESUMEN.md](RESUMEN.md)** - Resumen ejecutivo del proyecto y estado actual

### 🛠️ Scripts y Herramientas
- **[install.sh](install.sh)** - Script de instalación automatizado
- **[create_all_apps.py](create_all_apps.py)** - Generador automático de aplicaciones

---

## 🚀 Características Principales

### Módulos Implementados

- **RF-001**: Gestión de Vacantes
- **RF-002**: Selección de Estudiantes
- **RF-003**: Gestión de Documentación
- **RF-004**: Contratos y Convenios
- **RF-005**: Asignación de Tutores
- **RF-006**: Encuestas de Satisfacción
- **RF-007**: Reportes de Gestión
- **RF-008**: Seguimiento Semanal
- **RF-009**: Evaluaciones de Tutores
- **RF-010**: Cierre de Prácticas
- **RF-011**: Autenticación y Roles (JWT)
- **RF-012**: Registro de Estudiantes
- **RF-013**: Asignación de Profesor y Empresa
- **RF-014**: Observaciones del Profesor

## 🛠 Tecnologías

- **Backend**: Django 4.2, Django REST Framework
- **Base de Datos**: PostgreSQL 15
- **Autenticación**: JWT (SimpleJWT)
- **Tareas Asíncronas**: Celery + Redis
- **Caché**: Redis
- **Generación de PDFs**: WeasyPrint
- **Almacenamiento**: Django Storages + AWS S3 (opcional)
- **Seguridad**: Django Axes, CORS Headers

## 📋 Requisitos Previos

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (opcional)

## 🔧 Instalación

### Opción 1: Instalación Local

1. **Clonar el repositorio**
```bash
cd /Users/editsongutierreza/Downloads/nuclear
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En macOS/Linux
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Configurar PostgreSQL**
```bash
createdb practicas_db
```

6. **Ejecutar migraciones**
```bash
python manage.py migrate
```

7. **Crear superusuario**
```bash
python manage.py createsuperuser
```

8. **Cargar datos iniciales (opcional)**
```bash
python manage.py loaddata fixtures/initial_data.json
```

9. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

10. **En otra terminal, ejecutar Celery Worker**
```bash
celery -A config worker -l info
```

11. **En otra terminal, ejecutar Celery Beat**
```bash
celery -A config beat -l info
```

### Opción 2: Con Docker

1. **Configurar variables de entorno**
```bash
cp .env.example .env
```

2. **Construir y levantar contenedores**
```bash
docker-compose up --build
```

3. **Ejecutar migraciones**
```bash
docker-compose exec web python manage.py migrate
```

4. **Crear superusuario**
```bash
docker-compose exec web python manage.py createsuperuser
```

## 📁 Estructura del Proyecto

```
nuclear/
├── config/                 # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── apps/
│   ├── usuarios/          # RF-011, RF-012
│   ├── vacantes/          # RF-001
│   ├── postulaciones/     # RF-002
│   ├── documentos/        # RF-003
│   ├── contratos/         # RF-004
│   ├── tutores/           # RF-005
│   ├── encuestas/         # RF-006
│   ├── reportes/          # RF-007
│   ├── seguimiento/       # RF-008
│   ├── evaluaciones/      # RF-009
│   ├── cierre/            # RF-010
│   ├── practicas/         # RF-013
│   └── observaciones/     # RF-014
├── media/                 # Archivos subidos
├── static/                # Archivos estáticos
├── templates/             # Plantillas HTML/PDF
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```

## 🔑 Roles y Permisos

- **COORDINADOR**: Acceso completo al sistema
- **PROFESOR**: Gestión de sus estudiantes asignados
- **ESTUDIANTE**: Acceso a sus prácticas y documentación

## 🌐 API Endpoints Principales

### Autenticación
- `POST /api/auth/login/` - Login JWT
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/logout/` - Logout

### Vacantes
- `GET/POST /api/vacantes/` - Listar/Crear vacantes
- `GET/PUT/DELETE /api/vacantes/{id}/` - Detalle/Editar/Eliminar

### Estudiantes
- `POST /api/usuarios/estudiantes/` - Registrar estudiante (Coordinador)
- `GET /api/usuarios/estudiantes/` - Listar estudiantes

### Prácticas
- `POST /api/practicas/{id}/asignar/` - Asignar profesor y empresa
- `GET /api/practicas/` - Listar prácticas

### Postulaciones
- `POST /api/postulaciones/{id}/seleccionar/` - Seleccionar estudiante

### Observaciones
- `POST /api/observaciones/` - Crear observación (Profesor)
- `GET /api/observaciones/?practica={id}` - Ver observaciones

### Documentos
- `POST /api/documentos/` - Subir documento
- `GET /api/documentos/` - Listar documentos

### Reportes
- `GET /api/reportes/kpis/` - KPIs de gestión
- `POST /api/reportes/generar/` - Generar reporte async

## 🔒 Seguridad

- Autenticación JWT con tokens de acceso y refresh
- Protección contra fuerza bruta (Django Axes)
- CORS configurado
- Validación de archivos (MIME type, hash)
- Permisos granulares por rol

## 📧 Notificaciones

El sistema envía notificaciones por email para:
- Selección de estudiantes
- Asignación de prácticas
- Recordatorios de reportes semanales
- Recordatorios de encuestas
- Alertas de seguimiento

## 🧪 Testing

```bash
pytest
pytest --cov=apps
```

## 📊 Monitoreo

- Logs en `logs/django.log`
- Integración con Sentry (opcional)
- Panel de administración: `/admin/`

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es privado y confidencial.

## 👥 Contacto

Para soporte o consultas, contactar al equipo de desarrollo.

---

**Desarrollado con ❤️ usando Django y DRF**
