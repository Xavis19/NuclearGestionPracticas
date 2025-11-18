# 📑 ÍNDICE GENERAL DEL PROYECTO
# Sistema de Gestión de Prácticas Profesionales

¡Bienvenido! Este es el índice completo de la documentación del proyecto.

---

## 🎯 ¿QUÉ BUSCO?

### 👨‍💻 Soy Desarrollador - ¿Cómo empiezo?
**→ Lee: [INICIO_RAPIDO.md](INICIO_RAPIDO.md)**
- Instalación en 5 minutos
- Primeros pasos
- Ejemplos de código

### 📊 Soy Project Manager - ¿Qué incluye el proyecto?
**→ Lee: [RESUMEN.md](RESUMEN.md)**
- Estado actual del proyecto
- Funcionalidades implementadas
- Métricas y estadísticas
- Roadmap

### 🏗️ Necesito entender la arquitectura
**→ Lee: [ARQUITECTURA.md](ARQUITECTURA.md)**
- Diagrama de arquitectura
- Modelos de datos
- Sistema de permisos
- Flujos de trabajo
- Endpoints completos

### 📖 Necesito instrucciones detalladas
**→ Lee: [INSTRUCCIONES.md](INSTRUCCIONES.md)**
- Instalación paso a paso
- Ejemplos de uso de la API
- Solución de problemas
- Testing

### 🐳 Quiero usar Docker
**→ Lee: [README.md](README.md) - Sección Docker**
```bash
docker-compose up --build
```

---

## 📂 ESTRUCTURA DE LA DOCUMENTACIÓN

### Documentos Principales

| Documento | Propósito | Audiencia | Tiempo de Lectura |
|-----------|-----------|-----------|-------------------|
| **[INDEX.md](INDEX.md)** | Navegación general | Todos | 2 min |
| **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** | Instalación rápida | Desarrolladores | 5 min |
| **[README.md](README.md)** | Información general | Todos | 10 min |
| **[INSTRUCCIONES.md](INSTRUCCIONES.md)** | Guía detallada | Desarrolladores | 30 min |
| **[ARQUITECTURA.md](ARQUITECTURA.md)** | Arquitectura técnica | Arquitectos/Devs | 45 min |
| **[RESUMEN.md](RESUMEN.md)** | Resumen ejecutivo | PM/Stakeholders | 15 min |

### Archivos de Configuración

| Archivo | Descripción |
|---------|-------------|
| **[requirements.txt](requirements.txt)** | Dependencias Python |
| **[.env.example](.env.example)** | Variables de entorno template |
| **[docker-compose.yml](docker-compose.yml)** | Configuración Docker |
| **[Dockerfile](Dockerfile)** | Imagen Docker |

### Scripts de Utilidad

| Script | Descripción | Uso |
|--------|-------------|-----|
| **[install.sh](install.sh)** | Instalación automatizada | `./install.sh` |
| **[create_all_apps.py](create_all_apps.py)** | Generar apps | `python3 create_all_apps.py` |
| **[generate_apps.py](generate_apps.py)** | Generador alternativo | `python3 generate_apps.py` |

---

## 🗂️ MAPA DE APLICACIONES

### ✅ Apps Completamente Implementadas

#### 1. **apps/usuarios/** (RF-011, RF-012)
**Autenticación y Gestión de Usuarios**

Archivos clave:
- `models.py` - Custom User model con roles (COORDINADOR, PROFESOR, ESTUDIANTE)
- `serializers.py` - 5 serializers (User, Estudiante, Profesor, Coordinador, ChangePassword)
- `views.py` - 4 ViewSets con permisos por rol
- `permissions.py` - 6 clases de permisos personalizados
- `urls.py` - Routers configurados
- `admin.py` - Admin personalizado

Endpoints principales:
```
POST   /api/auth/login/
POST   /api/auth/refresh/
GET    /api/usuarios/users/me/
POST   /api/usuarios/estudiantes/
GET    /api/usuarios/profesores/
```

#### 2. **apps/vacantes/** (RF-001)
**Gestión de Empresas y Vacantes**

Archivos clave:
- `models.py` - Empresa, Vacante con validaciones
- `serializers.py` - EmpresaSerializer, VacanteSerializer
- `views.py` - ViewSets con filtros avanzados
- `admin.py` - Admin con fieldsets detallados

Endpoints principales:
```
GET/POST  /api/vacantes/empresas/
GET/POST  /api/vacantes/
GET       /api/vacantes/disponibles/
POST      /api/vacantes/{id}/verificar_requisitos/
```

#### 3. **apps/practicas/** (RF-013)
**Asignación de Prácticas**

Archivos clave:
- `models.py` - Practica con constraints únicos
- `views.py` - Asignación con validaciones (via create_all_apps.py)
- `tasks.py` - Notificaciones Celery

Endpoints principales:
```
GET/POST  /api/practicas/
POST      /api/practicas/{id}/asignar/
```

#### 4. **apps/postulaciones/** (RF-002)
**Postulaciones de Estudiantes**

Archivos clave:
- `models.py` - Postulacion (via create_all_apps.py)
- `views.py` - Selección de estudiantes
- `tasks.py` - Notificaciones

Endpoints principales:
```
GET/POST  /api/postulaciones/
POST      /api/postulaciones/{id}/seleccionar/
```

#### 5. **apps/observaciones/** (RF-014)
**Observaciones del Profesor**

Archivos clave:
- `models.py` - Observacion con timestamps (via create_all_apps.py)

Endpoints principales:
```
GET/POST  /api/observaciones/
GET       /api/observaciones/?practica={id}
```

### 🔧 Apps con Estructura Básica

Estas apps tienen la estructura creada pero requieren implementación completa:

- **apps/documentos/** (RF-003) - Gestión de documentos
- **apps/contratos/** (RF-004) - Generación de contratos
- **apps/tutores/** (RF-005) - Asignación de tutores
- **apps/encuestas/** (RF-006) - Encuestas de satisfacción
- **apps/reportes/** (RF-007) - Reportes y KPIs
- **apps/seguimiento/** (RF-008) - Seguimiento semanal
- **apps/evaluaciones/** (RF-009) - Evaluaciones
- **apps/cierre/** (RF-010) - Cierre de prácticas

Para implementar estas apps, ejecutar:
```bash
python3 create_all_apps.py
```

---

## 🚦 FLUJO DE TRABAJO RECOMENDADO

### Primer Día
1. **Leer**: [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
2. **Instalar**: Ejecutar `./install.sh` o instalar manualmente
3. **Explorar**: Admin panel en http://localhost:8000/admin/
4. **Probar**: API con Postman/curl

### Primera Semana
1. **Estudiar**: [ARQUITECTURA.md](ARQUITECTURA.md)
2. **Desarrollar**: Implementar apps faltantes usando create_all_apps.py
3. **Testear**: Crear tests unitarios
4. **Documentar**: Actualizar documentación

### Primer Mes
1. **Frontend**: Conectar con React/Vue/Angular
2. **Deploy**: Configurar servidor de producción
3. **CI/CD**: Implementar pipeline
4. **Monitoreo**: Configurar Sentry y logging

---

## 📊 REQUISITOS FUNCIONALES (RF)

| RF | Nombre | Estado | App | Documentación |
|----|--------|--------|-----|---------------|
| RF-001 | Vacantes | ✅ Completo | vacantes | ARQUITECTURA.md |
| RF-002 | Selección de Estudiantes | ✅ Completo | postulaciones | ARQUITECTURA.md |
| RF-003 | Documentación | 🔧 Básico | documentos | - |
| RF-004 | Contratos/Convenios | 🔧 Básico | contratos | - |
| RF-005 | Asignación de Tutores | 🔧 Básico | tutores | - |
| RF-006 | Satisfacción Estudiantes | 🔧 Básico | encuestas | - |
| RF-007 | Reportes de Gestión | 🔧 Básico | reportes | - |
| RF-008 | Seguimiento Semanal | 🔧 Básico | seguimiento | - |
| RF-009 | Evaluaciones de Tutores | 🔧 Básico | evaluaciones | - |
| RF-010 | Cierre de Prácticas | 🔧 Básico | cierre | - |
| RF-011 | Autenticación y Roles | ✅ Completo | usuarios | ARQUITECTURA.md |
| RF-012 | Registro de Estudiantes | ✅ Completo | usuarios | ARQUITECTURA.md |
| RF-013 | Asignación Profesor/Empresa | ✅ Completo | practicas | ARQUITECTURA.md |
| RF-014 | Observaciones del Profesor | ✅ Completo | observaciones | ARQUITECTURA.md |

**Leyenda:**
- ✅ Completo: Implementación funcional completa
- 🔧 Básico: Estructura creada, requiere implementación

---

## 🛠️ STACK TECNOLÓGICO

### Backend
- Python 3.11+
- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL 15+
- Redis 7+
- Celery 5.3.4

### Autenticación
- djangorestframework-simplejwt 5.3.0
- django-axes 6.1.1 (anti fuerza bruta)

### Storage & Files
- django-storages 1.14.2 (S3)
- WeasyPrint 60.1 (PDFs)
- python-docx 1.1.0

### Testing
- pytest 7.4.3
- pytest-django 4.7.0
- factory-boy 3.3.0

Ver [requirements.txt](requirements.txt) para la lista completa.

---

## 🎯 CASOS DE USO PRINCIPALES

### Caso 1: Coordinador Registra Estudiante
```
1. Coordinador hace login → Obtiene JWT
2. POST /api/usuarios/estudiantes/ con datos
3. Sistema valida y crea estudiante
4. Retorna datos del estudiante creado
```
**Ver**: [INSTRUCCIONES.md#registro-de-estudiantes](INSTRUCCIONES.md)

### Caso 2: Estudiante se Postula a Vacante
```
1. Estudiante hace login
2. GET /api/vacantes/disponibles/
3. POST /api/vacantes/{id}/verificar_requisitos/
4. POST /api/postulaciones/ con motivación
5. Sistema crea postulación
```
**Ver**: [ARQUITECTURA.md#flujo-de-postulación](ARQUITECTURA.md)

### Caso 3: Coordinador Asigna Práctica
```
1. Coordinador crea práctica
2. POST /api/practicas/{id}/asignar/ con profesor_id y empresa_id
3. Sistema valida cupos y empresa activa
4. Asigna y envía notificaciones
```
**Ver**: [ARQUITECTURA.md#flujo-de-asignación](ARQUITECTURA.md)

---

## 🆘 AYUDA RÁPIDA

### ❓ Problemas Comunes

| Problema | Solución | Documentación |
|----------|----------|---------------|
| Error al instalar | Ver INICIO_RAPIDO.md - Solución de problemas | [INICIO_RAPIDO.md](INICIO_RAPIDO.md) |
| Error de base de datos | Verificar PostgreSQL activo | [INSTRUCCIONES.md](INSTRUCCIONES.md) |
| Error de importación | Activar venv y reinstalar | [INICIO_RAPIDO.md](INICIO_RAPIDO.md) |
| 401 Unauthorized | Verificar JWT token | [INSTRUCCIONES.md](INSTRUCCIONES.md) |
| 403 Forbidden | Verificar permisos del rol | [ARQUITECTURA.md](ARQUITECTURA.md) |

### 🔍 Búsqueda Rápida

- **¿Cómo crear un usuario?** → INSTRUCCIONES.md #Gestión de Estudiantes
- **¿Qué endpoints existen?** → ARQUITECTURA.md #Endpoints Principales
- **¿Cómo funciona JWT?** → ARQUITECTURA.md #Sistema de Autenticación
- **¿Qué permisos tiene cada rol?** → ARQUITECTURA.md #Matriz de Permisos
- **¿Cómo ejecutar tests?** → INSTRUCCIONES.md #Testing

---

## 📞 SIGUIENTE PASO

### Para empezar AHORA:
```bash
# 1. Clonar/Navegar al proyecto
cd /Users/editsongutierreza/Downloads/nuclear

# 2. Leer guía rápida
cat INICIO_RAPIDO.md

# 3. Ejecutar instalación
./install.sh

# 4. Generar apps
python3 create_all_apps.py

# 5. Iniciar servidor
python manage.py runserver
```

### Para entender el proyecto:
1. Leer [RESUMEN.md](RESUMEN.md) (15 min)
2. Leer [ARQUITECTURA.md](ARQUITECTURA.md) (45 min)
3. Experimentar con la API usando [INSTRUCCIONES.md](INSTRUCCIONES.md)

---

## 📝 NOTAS IMPORTANTES

- ⚠️ **Los errores de importación en el IDE son normales** - Se resolverán al instalar las dependencias
- 📧 **Las notificaciones por email requieren** configurar SMTP en .env y activar Celery
- 🔐 **En producción**, cambiar SECRET_KEY y contraseñas por defecto
- 🐳 **Docker es la forma más fácil** de ejecutar el proyecto completo
- 🧪 **Crear tests** es altamente recomendado antes de producción

---

## 🎓 RECURSOS ADICIONALES

- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Celery Docs**: https://docs.celeryproject.org/
- **JWT.io**: https://jwt.io/

---

**🚀 ¡El proyecto está listo para usarse!**

Comienza con [INICIO_RAPIDO.md](INICIO_RAPIDO.md) y en 5 minutos tendrás el sistema ejecutándose.
