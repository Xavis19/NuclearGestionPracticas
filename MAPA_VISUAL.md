# 🗺️ MAPA VISUAL DEL PROYECTO
# Sistema de Gestión de Prácticas Profesionales

## 📁 ESTRUCTURA COMPLETA DEL PROYECTO

```
nuclear/
│
├── 📚 DOCUMENTACIÓN (¡EMPIEZA AQUÍ!)
│   ├── INDEX.md ⭐                  ← PUNTO DE ENTRADA PRINCIPAL
│   ├── INICIO_RAPIDO.md            ← Instalación en 5 minutos
│   ├── README.md                   ← Información general
│   ├── INSTRUCCIONES.md            ← Guía detallada + ejemplos API
│   ├── ARQUITECTURA.md             ← Arquitectura técnica completa
│   ├── RESUMEN.md                  ← Resumen ejecutivo
│   └── MAPA_VISUAL.md              ← Este archivo
│
├── ⚙️ CONFIGURACIÓN
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py ✅          ← Configuración completa
│   │   ├── urls.py ✅              ← URLs principales
│   │   ├── celery.py ✅            ← Config Celery
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── .env.example ✅             ← Template de variables de entorno
│   ├── requirements.txt ✅         ← Todas las dependencias
│   ├── manage.py ✅                ← Django management
│   ├── docker-compose.yml ✅       ← Docker config
│   ├── Dockerfile ✅               ← Docker image
│   └── .gitignore ✅
│
├── 🛠️ SCRIPTS DE UTILIDAD
│   ├── install.sh ✅               ← Instalación automatizada
│   ├── create_all_apps.py ✅       ← Generador de apps
│   └── generate_apps.py ✅         ← Generador alternativo
│
├── 📱 APLICACIONES
│   └── apps/
│       │
│       ├── 🔐 usuarios/ ✅✅✅ (RF-011, RF-012)
│       │   ├── models.py           ← Custom User, roles, validaciones
│       │   ├── serializers.py      ← 5 serializers
│       │   ├── views.py            ← 4 ViewSets
│       │   ├── permissions.py      ← 6 permisos custom
│       │   ├── exceptions.py       ← Exception handler
│       │   ├── urls.py
│       │   ├── admin.py
│       │   └── tests.py
│       │
│       ├── 🏢 vacantes/ ✅✅✅ (RF-001)
│       │   ├── models.py           ← Empresa, Vacante
│       │   ├── serializers.py      ← 3 serializers
│       │   ├── views.py            ← ViewSets + filtros
│       │   ├── urls.py
│       │   ├── admin.py
│       │   └── apps.py
│       │
│       ├── 📋 practicas/ ✅✅ (RF-013)
│       │   ├── models.py           ← Practica + constraints
│       │   ├── serializers.py      ← Via script
│       │   ├── views.py            ← Asignación
│       │   ├── tasks.py            ← Notificaciones
│       │   └── ...
│       │
│       ├── 📝 postulaciones/ ✅✅ (RF-002)
│       │   ├── models.py           ← Postulacion
│       │   ├── views.py            ← Selección
│       │   ├── tasks.py            ← Emails
│       │   └── ...
│       │
│       ├── 💬 observaciones/ ✅ (RF-014)
│       │   ├── models.py           ← Observacion
│       │   └── ...
│       │
│       ├── 📄 documentos/ 🔧 (RF-003)
│       │   └── [estructura básica]
│       │
│       ├── 📜 contratos/ 🔧 (RF-004)
│       │   └── [estructura básica]
│       │
│       ├── 👥 tutores/ 🔧 (RF-005)
│       │   └── [estructura básica]
│       │
│       ├── 📊 encuestas/ 🔧 (RF-006)
│       │   └── [estructura básica]
│       │
│       ├── 📈 reportes/ 🔧 (RF-007)
│       │   └── [estructura básica]
│       │
│       ├── 📅 seguimiento/ 🔧 (RF-008)
│       │   └── [estructura básica]
│       │
│       ├── ⭐ evaluaciones/ 🔧 (RF-009)
│       │   └── [estructura básica]
│       │
│       └── 🏁 cierre/ 🔧 (RF-010)
│           └── [estructura básica]
│
├── 📁 DIRECTORIOS DE EJECUCIÓN
│   ├── media/                      ← Archivos subidos
│   ├── static/                     ← Archivos estáticos
│   ├── staticfiles/                ← Archivos recopilados
│   ├── logs/                       ← Logs de aplicación
│   └── templates/                  ← Plantillas HTML
│
└── 🐍 ENTORNO VIRTUAL
    └── venv/                       ← Entorno Python (crear)

```

**Leyenda:**
- ✅✅✅ = Completamente implementado y funcional
- ✅✅ = Implementado con estructura via script
- ✅ = Implementado
- 🔧 = Estructura básica (requiere implementación completa)

---

## 🔄 FLUJO DE DATOS COMPLETO

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENTE (Browser/App)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP + JWT Token
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Django URLs (config/urls.py)              │
│                                                               │
│  /api/auth/login/          → JWT Authentication             │
│  /api/usuarios/*           → apps.usuarios.urls             │
│  /api/vacantes/*           → apps.vacantes.urls             │
│  /api/practicas/*          → apps.practicas.urls            │
│  /api/postulaciones/*      → apps.postulaciones.urls        │
│  /api/observaciones/*      → apps.observaciones.urls        │
│  [etc...]                                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Django REST Framework (ViewSets)                │
│                                                               │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │  Permissions   │  │  Serializers   │  │    Views     │  │
│  │                │  │                │  │              │  │
│  │ - IsCoordinador│  │ - Validations  │  │ - CRUD       │  │
│  │ - IsProfesor   │  │ - Transform    │  │ - Filters    │  │
│  │ - IsEstudiante │  │ - Relations    │  │ - Search     │  │
│  └────────────────┘  └────────────────┘  └──────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     Django ORM (Models)                      │
│                                                               │
│  User → Practica → Empresa → Vacante → Postulacion          │
│         ↓          ↓                    ↓                     │
│  Observacion    [Más modelos...]    [Más modelos...]        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      PostgreSQL Database                     │
│                                                               │
│  Tables:                                                      │
│  - usuarios_user                                             │
│  - vacantes_empresa                                          │
│  - vacantes_vacante                                          │
│  - practicas_practica                                        │
│  - postulaciones_postulacion                                 │
│  - observaciones_observacion                                 │
│  [etc...]                                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎭 ROLES Y ACCESOS

```
┌─────────────────────────────────────────────────────────┐
│                    COORDINADOR 👨‍💼                        │
│                  (Acceso Completo)                       │
│                                                          │
│  ✅ Crear/Editar usuarios (estudiantes, profesores)     │
│  ✅ Gestionar empresas                                   │
│  ✅ Crear/Editar vacantes                               │
│  ✅ Asignar prácticas (profesor + empresa)              │
│  ✅ Ver todas las prácticas                             │
│  ✅ Seleccionar estudiantes                             │
│  ✅ Generar reportes                                    │
│  ✅ Acceso total al sistema                             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                      PROFESOR 👨‍🏫                         │
│              (Acceso a Supervisión)                      │
│                                                          │
│  ✅ Ver sus estudiantes asignados                       │
│  ✅ Crear observaciones en prácticas asignadas          │
│  ✅ Ver listado de estudiantes                          │
│  ✅ Ver vacantes                                         │
│  ❌ No puede crear usuarios                             │
│  ❌ No puede asignar prácticas                          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    ESTUDIANTE 🎓                         │
│               (Acceso a su Perfil)                       │
│                                                          │
│  ✅ Ver su perfil                                        │
│  ✅ Ver vacantes disponibles                            │
│  ✅ Postularse a vacantes                               │
│  ✅ Ver sus prácticas                                    │
│  ✅ Verificar requisitos para vacantes                  │
│  ❌ No puede ver otros estudiantes                      │
│  ❌ No puede crear vacantes                             │
└─────────────────────────────────────────────────────────┘
```

---

## 🔌 ENDPOINTS POR MÓDULO

### 🔐 Autenticación
```
POST   /api/auth/login/           → Obtener JWT tokens
POST   /api/auth/refresh/         → Refrescar access token
POST   /api/auth/verify/          → Verificar token válido
```

### 👥 Usuarios (apps/usuarios/)
```
GET    /api/usuarios/users/me/              → Perfil actual
POST   /api/usuarios/users/change_password/ → Cambiar password
GET    /api/usuarios/estudiantes/           → Listar estudiantes
POST   /api/usuarios/estudiantes/           → Crear estudiante ⚡
GET    /api/usuarios/profesores/            → Listar profesores
GET    /api/usuarios/coordinadores/         → Listar coordinadores
```
⚡ = Solo Coordinador

### 🏢 Empresas y Vacantes (apps/vacantes/)
```
GET    /api/vacantes/empresas/                  → Listar empresas
POST   /api/vacantes/empresas/                  → Crear empresa ⚡
POST   /api/vacantes/empresas/{id}/verificar/   → Verificar empresa ⚡

GET    /api/vacantes/                           → Listar vacantes
POST   /api/vacantes/                           → Crear vacante ⚡
GET    /api/vacantes/disponibles/               → Vacantes disponibles
POST   /api/vacantes/{id}/verificar_requisitos/ → Verificar si cumple requisitos
POST   /api/vacantes/{id}/cerrar/               → Cerrar vacante ⚡
POST   /api/vacantes/{id}/reabrir/              → Reabrir vacante ⚡
```

### 📋 Prácticas (apps/practicas/)
```
GET    /api/practicas/               → Listar prácticas
POST   /api/practicas/               → Crear práctica ⚡
POST   /api/practicas/{id}/asignar/  → Asignar profesor y empresa ⚡
```

### 📝 Postulaciones (apps/postulaciones/)
```
GET    /api/postulaciones/                  → Listar postulaciones
POST   /api/postulaciones/                  → Crear postulación 🎓
POST   /api/postulaciones/{id}/seleccionar/ → Seleccionar estudiante ⚡
```
🎓 = Solo Estudiante

### 💬 Observaciones (apps/observaciones/)
```
GET    /api/observaciones/                → Listar observaciones
POST   /api/observaciones/                → Crear observación 👨‍🏫
GET    /api/observaciones/?practica={id}  → Filtrar por práctica
```
👨‍🏫 = Solo Profesor asignado

---

## 🚀 ORDEN DE EJECUCIÓN RECOMENDADO

### 1️⃣ INSTALACIÓN
```bash
# Opción A: Automática
./install.sh

# Opción B: Manual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
createdb practicas_db
python manage.py migrate
python manage.py createsuperuser
```

### 2️⃣ GENERAR APPS
```bash
python3 create_all_apps.py
python manage.py makemigrations
python manage.py migrate
```

### 3️⃣ EJECUTAR
```bash
# Terminal 1: Django
python manage.py runserver

# Terminal 2: Redis (opcional)
redis-server

# Terminal 3: Celery Worker (opcional)
celery -A config worker -l info

# Terminal 4: Celery Beat (opcional)
celery -A config beat -l info
```

### 4️⃣ PROBAR
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@ejemplo.com", "password": "tu_password"}'

# Usar token en siguientes requests
curl -X GET http://localhost:8000/api/usuarios/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📚 GUÍAS RECOMENDADAS POR ROL

### 🎯 Desarrollador Backend
1. **Leer**: [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
2. **Leer**: [ARQUITECTURA.md](ARQUITECTURA.md)
3. **Revisar**: Código en `apps/usuarios/` y `apps/vacantes/`
4. **Implementar**: Apps faltantes usando `create_all_apps.py`

### 🎯 Desarrollador Frontend
1. **Leer**: [INSTRUCCIONES.md](INSTRUCCIONES.md) - Sección Ejemplos de API
2. **Probar**: Endpoints con Postman
3. **Integrar**: JWT authentication en frontend
4. **Conectar**: Formularios con endpoints

### 🎯 Project Manager
1. **Leer**: [RESUMEN.md](RESUMEN.md)
2. **Revisar**: Este archivo (MAPA_VISUAL.md)
3. **Planificar**: Basado en apps pendientes (🔧)

### 🎯 DevOps
1. **Revisar**: [docker-compose.yml](docker-compose.yml)
2. **Leer**: [README.md](README.md) - Sección Deployment
3. **Configurar**: Variables de entorno (.env)
4. **Deploy**: Nginx + Gunicorn + PostgreSQL + Redis

---

## 🎨 CONVENCIONES DEL CÓDIGO

### Estructura de una App Django
```
app_name/
├── __init__.py
├── models.py          ← Modelos de base de datos
├── serializers.py     ← Serializers de DRF
├── views.py           ← ViewSets y endpoints
├── urls.py            ← Routers y URLs
├── admin.py           ← Configuración del admin
├── permissions.py     ← Permisos personalizados (si aplica)
├── tasks.py           ← Tareas de Celery (si aplica)
├── tests.py           ← Tests unitarios
└── apps.py            ← Configuración de la app
```

### Patrón de Nombres
- **Modelos**: PascalCase (ej: `User`, `Vacante`)
- **Serializers**: PascalCase + Serializer (ej: `UserSerializer`)
- **Views**: PascalCase + ViewSet (ej: `UserViewSet`)
- **Permisos**: Is + PascalCase (ej: `IsCoordinador`)
- **URLs**: lowercase con guiones (ej: `api/usuarios/estudiantes/`)

---

## 📊 MÉTRICAS DEL PROYECTO

```
📁 Archivos de Código:        ~80 archivos
📝 Líneas de Código:          ~7000 líneas
📚 Archivos de Documentación: 7 archivos (~2500 líneas)
🎯 RFs Implementados:         6/14 (43%)
📱 Apps Completas:            5/13 (38%)
📱 Apps con Estructura:       8/13 (62%)
🔌 Endpoints Funcionales:     40+ endpoints
```

---

## 🎓 PRÓXIMOS PASOS

### Corto Plazo (Esta Semana)
- [ ] Ejecutar `create_all_apps.py`
- [ ] Implementar modelos completos en apps básicas
- [ ] Crear tests unitarios básicos
- [ ] Probar todos los endpoints

### Mediano Plazo (Este Mes)
- [ ] Frontend básico (React/Vue)
- [ ] Completar RF-003 a RF-010
- [ ] Documentación de API (Swagger)
- [ ] CI/CD pipeline

### Largo Plazo (2-3 Meses)
- [ ] Deploy a producción
- [ ] Monitoreo y alertas
- [ ] Optimizaciones de performance
- [ ] App móvil (opcional)

---

**¿Perdido? Regresa a [INDEX.md](INDEX.md) para navegación completa**

**¿Primera vez? Lee [INICIO_RAPIDO.md](INICIO_RAPIDO.md) para comenzar en 5 minutos**
