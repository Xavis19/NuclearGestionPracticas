# ARQUITECTURA DEL SISTEMA
# Sistema de Gestión de Prácticas Profesionales

## 📋 DIAGRAMA DE ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Frontend)                        │
│                    React / Vue / Angular                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP/HTTPS + JWT
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NGINX (Reverse Proxy)                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DJANGO REST FRAMEWORK                         │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                     AUTENTICACIÓN JWT                        │ │
│ │  Simple JWT + Django Axes (Anti fuerza bruta)               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                        APLICACIONES                          │ │
│ │                                                              │ │
│ │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │ │
│ │  │ Usuarios   │  │ Vacantes   │  │ Prácticas  │            │ │
│ │  │ (RF-11/12) │  │  (RF-01)   │  │  (RF-13)   │            │ │
│ │  └────────────┘  └────────────┘  └────────────┘            │ │
│ │                                                              │ │
│ │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │ │
│ │  │Postulacion │  │Observacion │  │ Documentos │            │ │
│ │  │  (RF-02)   │  │  (RF-14)   │  │  (RF-03)   │            │ │
│ │  └────────────┘  └────────────┘  └────────────┘            │ │
│ │                                                              │ │
│ │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │ │
│ │  │ Contratos  │  │  Tutores   │  │ Encuestas  │            │ │
│ │  │  (RF-04)   │  │  (RF-05)   │  │  (RF-06)   │            │ │
│ │  └────────────┘  └────────────┘  └────────────┘            │ │
│ │                                                              │ │
│ │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │ │
│ │  │ Reportes   │  │Seguimiento │  │Evaluaciones│            │ │
│ │  │  (RF-07)   │  │  (RF-08)   │  │  (RF-09)   │            │ │
│ │  └────────────┘  └────────────┘  └────────────┘            │ │
│ │                                                              │ │
│ │  ┌────────────┐                                             │ │
│ │  │   Cierre   │                                             │ │
│ │  │  (RF-10)   │                                             │ │
│ │  └────────────┘                                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
└───────────┬───────────────┬───────────────┬─────────────────────┘
            │               │               │
            ▼               ▼               ▼
  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │  PostgreSQL  │ │    Redis     │ │   Celery     │
  │              │ │              │ │              │
  │ - Datos      │ │ - Cache      │ │ - Workers    │
  │ - Índices    │ │ - Sessions   │ │ - Beat       │
  │ - Triggers   │ │ - Broker     │ │ - Tasks      │
  └──────────────┘ └──────────────┘ └──────────────┘
            │               
            ▼               
  ┌──────────────┐          ┌──────────────┐
  │   AWS S3     │          │    Email     │
  │ (Producción) │          │   Service    │
  │              │          │              │
  │ - Documentos │          │ - SMTP       │
  │ - Reportes   │          │ - Celery     │
  │ - Contratos  │          │              │
  └──────────────┘          └──────────────┘
```

## 🗄️ MODELOS DE DATOS PRINCIPALES

### App: usuarios

```python
User (AbstractUser)
├── id (PK)
├── username (unique)
├── email (unique)
├── role: COORDINADOR | PROFESOR | ESTUDIANTE
├── first_name, last_name
├── phone
├── Para ESTUDIANTE:
│   ├── matricula (unique)
│   ├── carrera
│   ├── semestre
│   └── promedio
└── Para PROFESOR:
    ├── departamento
    └── especialidad
```

### App: vacantes

```python
Empresa
├── id (PK)
├── nombre, rfc (unique), razon_social
├── direccion, telefono, email, sitio_web
├── contacto_* (nombre, puesto, email, telefono)
├── sector, tamaño
├── activa, verificada
├── created_by (FK → User)
└── timestamps

Vacante
├── id (PK)
├── empresa (FK → Empresa)
├── titulo, descripcion, requisitos
├── carreras_solicitadas
├── semestre_minimo, promedio_minimo
├── area, modalidad, ubicacion
├── horario, duracion_meses
├── vacantes_disponibles, vacantes_ocupadas
├── fecha_inicio, fecha_cierre_convocatoria
├── remunerada, monto_apoyo, beneficios_adicionales
├── estado: ABIERTA | CERRADA | PAUSADA | CANCELADA
├── created_by (FK → User)
└── timestamps
```

### App: practicas

```python
Practica
├── id (PK)
├── estudiante (FK → User, ESTUDIANTE)
├── profesor (FK → User, PROFESOR)
├── empresa (FK → Empresa)
├── area_practica, proyecto
├── fecha_inicio, fecha_fin, fecha_asignacion
├── estado: PENDIENTE | ASIGNADA | EN_CURSO | COMPLETADA | CANCELADA
├── cerrada (boolean)
├── calificacion_final
├── asignada_por (FK → User, COORDINADOR)
├── timestamps
└── CONSTRAINT: unique_active_practica_per_estudiante
```

### App: postulaciones

```python
Postulacion
├── id (PK)
├── estudiante (FK → User)
├── vacante (FK → Vacante)
├── estado: PENDIENTE | SELECCIONADO | RECHAZADO
├── motivacion (TextField)
├── fecha_seleccion
├── seleccionado_por (FK → User)
├── timestamps
└── UNIQUE (estudiante, vacante)
```

### App: observaciones

```python
Observacion
├── id (PK)
├── practica (FK → Practica)
├── profesor (FK → User)
├── texto (TextField)
└── created_at
```

## 🔐 SISTEMA DE PERMISOS

### Matriz de Permisos

| Recurso              | COORDINADOR | PROFESOR | ESTUDIANTE |
|---------------------|-------------|----------|------------|
| **Usuarios**        |             |          |            |
| - Crear Estudiante  | ✅          | ❌       | ❌         |
| - Listar Estudiantes| ✅          | ✅ (Ver) | ❌         |
| - Ver Perfil Propio | ✅          | ✅       | ✅         |
| - Editar Perfil     | ✅          | ❌       | ❌         |
| **Empresas**        |             |          |            |
| - Crear/Editar      | ✅          | ❌       | ❌         |
| - Ver               | ✅          | ✅       | ✅         |
| - Verificar         | ✅          | ❌       | ❌         |
| **Vacantes**        |             |          |            |
| - Crear/Editar      | ✅          | ❌       | ❌         |
| - Ver Todas         | ✅          | ✅       | ❌         |
| - Ver Disponibles   | ✅          | ✅       | ✅         |
| - Verificar Requis. | ❌          | ❌       | ✅         |
| **Prácticas**       |             |          |            |
| - Crear             | ✅          | ❌       | ❌         |
| - Asignar           | ✅          | ❌       | ❌         |
| - Ver Todas         | ✅          | ❌       | ❌         |
| - Ver Asignadas     | ✅          | ✅       | ✅ (propia)|
| **Postulaciones**   |             |          |            |
| - Crear             | ❌          | ❌       | ✅         |
| - Seleccionar       | ✅          | ❌       | ❌         |
| - Ver               | ✅          | ✅       | ✅ (propia)|
| **Observaciones**   |             |          |            |
| - Crear             | ❌          | ✅ (asig)| ❌         |
| - Ver               | ✅          | ✅ (asig)| ✅ (propia)|

## 🔄 FLUJOS DE TRABAJO PRINCIPALES

### 1. Flujo de Asignación de Práctica (RF-013)

```
1. Coordinador crea práctica
   ↓
2. Coordinador asigna profesor y empresa
   ├── Validar empresa activa
   ├── Validar cupo del profesor (máx N estudiantes)
   └── Constraint: Estudiante solo puede tener 1 práctica activa
   ↓
3. Estado cambia a ASIGNADA
   ↓
4. Se envía notificación por email (Celery)
   ├── Email a estudiante
   └── Email a profesor
   ↓
5. Práctica inicia → estado EN_CURSO
```

### 2. Flujo de Postulación a Vacante (RF-001, RF-002)

```
1. Estudiante ve vacantes disponibles
   ↓
2. Estudiante verifica requisitos
   ├── Semestre mínimo
   ├── Promedio mínimo
   └── Carrera solicitada
   ↓
3. Estudiante crea postulación
   ├── Carta de motivación
   └── Estado: PENDIENTE
   ↓
4. Coordinador/Empresa revisa postulaciones
   ↓
5. Coordinador selecciona estudiante
   ├── Estado → SELECCIONADO
   ├── Incrementar vacantes_ocupadas en Vacante
   └── Si vacantes_restantes == 0 → Vacante.CERRADA
   ↓
6. Notificación por email (Celery)
```

### 3. Flujo de Registro de Estudiante (RF-012)

```
1. Coordinador accede a /api/usuarios/estudiantes/
   ↓
2. Envía datos del estudiante
   ├── Validar email único
   ├── Validar username único
   ├── Validar matrícula única (opcional)
   └── Validar contraseña (política de seguridad)
   ↓
3. Transacción atómica crea usuario
   ├── role = ESTUDIANTE
   ├── is_active = True
   └── Genera matrícula si no existe
   ↓
4. Email de bienvenida (Celery - opcional)
```

## 🎯 ENDPOINTS PRINCIPALES

### Autenticación
```
POST   /api/auth/login/          # Obtener JWT tokens
POST   /api/auth/refresh/        # Refrescar access token
POST   /api/auth/verify/         # Verificar token
```

### Usuarios
```
GET    /api/usuarios/users/me/              # Perfil del usuario actual
POST   /api/usuarios/users/change_password/ # Cambiar contraseña
GET    /api/usuarios/estudiantes/           # Listar estudiantes
POST   /api/usuarios/estudiantes/           # Crear estudiante (Coordinador)
GET    /api/usuarios/profesores/            # Listar profesores
GET    /api/usuarios/coordinadores/         # Listar coordinadores
```

### Empresas y Vacantes
```
GET    /api/vacantes/empresas/              # Listar empresas
POST   /api/vacantes/empresas/              # Crear empresa (Coordinador)
POST   /api/vacantes/empresas/{id}/verificar/ # Verificar empresa

GET    /api/vacantes/                       # Listar vacantes
POST   /api/vacantes/                       # Crear vacante (Coordinador)
GET    /api/vacantes/disponibles/           # Vacantes disponibles
POST   /api/vacantes/{id}/verificar_requisitos/ # Verificar requisitos
POST   /api/vacantes/{id}/cerrar/           # Cerrar vacante
POST   /api/vacantes/{id}/reabrir/          # Reabrir vacante
```

### Prácticas
```
GET    /api/practicas/                      # Listar prácticas
POST   /api/practicas/                      # Crear práctica
POST   /api/practicas/{id}/asignar/         # Asignar profesor y empresa
```

### Postulaciones
```
GET    /api/postulaciones/                  # Listar postulaciones
POST   /api/postulaciones/                  # Crear postulación
POST   /api/postulaciones/{id}/seleccionar/ # Seleccionar estudiante
```

### Observaciones
```
GET    /api/observaciones/                  # Listar observaciones
POST   /api/observaciones/                  # Crear observación
GET    /api/observaciones/?practica={id}    # Filtrar por práctica
```

## 🔧 TECNOLOGÍAS Y DEPENDENCIAS

### Core
- **Django 4.2**: Framework web
- **DRF**: API REST
- **PostgreSQL**: Base de datos
- **Redis**: Cache y broker
- **Celery**: Tareas asíncronas

### Autenticación & Seguridad
- **djangorestframework-simplejwt**: JWT tokens
- **django-axes**: Anti fuerza bruta
- **django-cors-headers**: CORS
- **django-environ**: Variables de entorno

### Storage & Files
- **django-storages**: S3 integration
- **boto3**: AWS SDK
- **django-cleanup**: Limpiar archivos huérfanos
- **python-magic**: Validación MIME

### Documentos & PDFs
- **WeasyPrint**: Generación de PDFs
- **python-docx**: Documentos Word
- **openpyxl**: Excel

### Auditoría & Versionado
- **django-simple-history**: Auditoría de modelos

### Filtros & Búsqueda
- **django-filter**: Filtros avanzados
- **django.contrib.postgres**: Búsqueda trigram (opcional)

## 📊 BASE DE DATOS

### Índices Principales

```sql
-- Usuarios
CREATE INDEX idx_user_email ON usuarios_user(email);
CREATE INDEX idx_user_role ON usuarios_user(role);
CREATE INDEX idx_user_matricula ON usuarios_user(matricula);

-- Vacantes
CREATE INDEX idx_vacante_empresa_estado ON vacantes_vacante(empresa_id, estado);
CREATE INDEX idx_vacante_estado_fecha ON vacantes_vacante(estado, fecha_cierre_convocatoria);

-- Prácticas
CREATE INDEX idx_practica_estudiante_estado ON practicas_practica(estudiante_id, estado);
CREATE INDEX idx_practica_profesor_estado ON practicas_practica(profesor_id, estado);
```

### Constraints

```sql
-- Un estudiante solo puede tener una práctica activa
ALTER TABLE practicas_practica
ADD CONSTRAINT unique_active_practica_per_estudiante
UNIQUE (estudiante_id)
WHERE (estado IN ('ASIGNADA', 'EN_CURSO'));

-- Una postulación única por estudiante y vacante
ALTER TABLE postulaciones_postulacion
ADD CONSTRAINT unique_estudiante_vacante
UNIQUE (estudiante_id, vacante_id);
```

## 🚀 DEPLOYMENT

### Producción con Gunicorn + Nginx

```bash
# Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Nginx config
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name practicas.universidad.edu;
    
    location /static/ {
        alias /path/to/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/media/;
    }
    
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Production

```yaml
version: '3.8'

services:
  web:
    image: practicas:latest
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:pass@db:5432/practicas_db
    depends_on:
      - db
      - redis
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./staticfiles:/staticfiles
```

## 📈 ESCALABILIDAD

### Optimizaciones Implementadas
- ✅ Índices en campos frecuentemente consultados
- ✅ Select related / prefetch related en queries
- ✅ Paginación en listados
- ✅ Cache con Redis
- ✅ Tareas asíncronas con Celery

### Optimizaciones Futuras
- [ ] Implementar cache en endpoints lentos
- [ ] Búsqueda full-text con PostgreSQL trigram
- [ ] CDN para archivos estáticos
- [ ] Particionamiento de tablas grandes
- [ ] Read replicas para PostgreSQL

---

**Arquitectura diseñada para escalabilidad y mantenibilidad**
