# 📋 ANÁLISIS DE REQUISITOS POR ROL - NuclearGestionPracticas

## Estado Actual vs Requisitos

### ✅ YA IMPLEMENTADO

#### Usuarios (apps/usuarios/)
- ✅ Modelo User con 3 roles: COORDINADOR, PROFESOR, ESTUDIANTE
- ✅ Campos de estudiante: matricula, carrera, semestre, promedio
- ✅ Campos de profesor: departamento, especialidad
- ✅ Autenticación con email O username (recién implementado)
- ✅ Sistema de permisos básico

#### Vacantes (apps/vacantes/)
- ✅ Modelo Vacante y Empresa
- ✅ COORDINADOR puede registrar vacantes
- ✅ Validación de requisitos (semestre, promedio, carrera)

#### Postulaciones (apps/postulaciones/)
- ✅ Modelo Postulacion
- ✅ ESTUDIANTE puede postularse a vacantes
- ✅ Estados: PENDIENTE, SELECCIONADO, RECHAZADO

#### Prácticas (apps/practicas/)
- ✅ Modelo Practica
- ✅ Asignación de profesor y empresa
- ✅ Estados: PENDIENTE, ASIGNADA, EN_CURSO, COMPLETADA, CANCELADA

#### Observaciones (apps/observaciones/)
- ✅ Modelo Observacion
- ✅ PROFESOR puede agregar observaciones sobre prácticas

#### Documentos (apps/documentos/)
- ✅ Modelo Documento básico
- ✅ Upload de archivos

---

## ❌ FALTA IMPLEMENTAR

### 1. ROL COORDINADOR (Falta 40%)

#### ✅ Ya tiene:
- Registrar estudiantes
- Registrar vacantes
- Asignar profesor y empresa a prácticas

#### ❌ Falta:
- [ ] **Verificar estudiantes** (campo `verificado` en modelo Estudiante)
- [ ] **Sistema de encuestas** completo
- [ ] **Enviar encuestas a todos los roles**
- [ ] Dashboard con estadísticas completas

---

### 2. ROL ESTUDIANTE (Falta 60%)

#### ✅ Ya tiene:
- Postularse a vacantes
- Ver prácticas asignadas

#### ❌ Falta:
- [ ] **Subir hoja de vida (CV)** - Campo `cv_file` en modelo User
- [ ] **Configuración de perfil** completa
- [ ] **Forgot password** (recuperación de contraseña)
- [ ] **Sistema de notificaciones**
  - [ ] Modelo Notificacion
  - [ ] Notificar cuando es seleccionado
  - [ ] Notificar cuando profesor agrega observación
  - [ ] Notificar encuestas nuevas
- [ ] **Activar/desactivar notificaciones** (preferencias)

---

### 3. ROL DOCENTE ASESOR (Falta 80%)

#### ✅ Ya tiene:
- Ver estudiantes asignados
- Agregar observaciones básicas

#### ❌ Falta:
- [ ] **Sistema de informes semanales**
  - [ ] Modelo InformeSemanal
  - [ ] Campos: fecha, descripción, avances, dificultades
  - [ ] Relación con Practica
- [ ] **Apartado de proyecto de práctica**
  - [ ] Campo `descripcion_proyecto` en Practica
  - [ ] Campo `objetivos` en Practica
  - [ ] Campo `actividades` en Practica
- [ ] **Sistema de evaluación continua**
  - [ ] Modelo EvaluacionContinua
  - [ ] Criterios de evaluación
  - [ ] Calificaciones parciales
  - [ ] Retroalimentación semanal

---

## 📊 PRIORIZACIÓN DE IMPLEMENTACIÓN

### FASE 1: ESENCIALES (Semana 1-2)
1. ✅ **Login funcional** (Ya resuelto)
2. 🔄 **Campo verificado para estudiantes**
3. 🔄 **Subir CV/Hoja de vida**
4. 🔄 **Sistema de notificaciones básico**
5. 🔄 **Forgot password**

### FASE 2: DOCENTE ASESOR (Semana 3)
6. 🔄 **Modelo InformeSemanal**
7. 🔄 **Campos de proyecto en Practica**
8. 🔄 **Modelo EvaluacionContinua**
9. 🔄 **Vista para subir informes semanales**

### FASE 3: ENCUESTAS (Semana 4)
10. 🔄 **Modelo Encuesta**
11. 🔄 **Modelo Respuesta**
12. 🔄 **Sistema de envío de encuestas**
13. 🔄 **Vista para responder encuestas**

### FASE 4: EXTRAS (Semana 5)
14. 🔄 **Dashboard completo para cada rol**
15. 🔄 **Reportes y estadísticas**
16. 🔄 **Preferencias de notificaciones**

---

## 🎯 MODELOS A CREAR

### 1. Notificaciones
```python
class Notificacion(models.Model):
    usuario = ForeignKey(User)
    tipo = CharField(choices=[...])  # POSTULACION, OBSERVACION, ENCUESTA, etc.
    titulo = CharField()
    mensaje = TextField()
    leida = BooleanField(default=False)
    url = CharField()  # URL para ir al detalle
    created_at = DateTimeField(auto_now_add=True)
```

### 2. Informes Semanales
```python
class InformeSemanal(models.Model):
    practica = ForeignKey(Practica)
    profesor = ForeignKey(User)
    semana = IntegerField()
    fecha_inicio = DateField()
    fecha_fin = DateField()
    actividades_realizadas = TextField()
    avances = TextField()
    dificultades = TextField()
    observaciones = TextField()
    archivo_adjunto = FileField()
    created_at = DateTimeField(auto_now_add=True)
```

### 3. Evaluaciones Continuas
```python
class EvaluacionContinua(models.Model):
    practica = ForeignKey(Practica)
    profesor = ForeignKey(User)
    periodo = CharField()  # "Semana 1-4", "Mes 1", etc.
    
    # Criterios de evaluación
    puntualidad = IntegerField(1-5)
    responsabilidad = IntegerField(1-5)
    calidad_trabajo = IntegerField(1-5)
    trabajo_equipo = IntegerField(1-5)
    iniciativa = IntegerField(1-5)
    
    calificacion = DecimalField()
    retroalimentacion = TextField()
    created_at = DateTimeField(auto_now_add=True)
```

### 4. Encuestas
```python
class Encuesta(models.Model):
    titulo = CharField()
    descripcion = TextField()
    creada_por = ForeignKey(User)  # COORDINADOR
    dirigida_a = CharField(choices=[...])  # TODOS, ESTUDIANTES, PROFESORES
    fecha_inicio = DateTimeField()
    fecha_fin = DateTimeField()
    activa = BooleanField()

class Pregunta(models.Model):
    encuesta = ForeignKey(Encuesta)
    texto = TextField()
    tipo = CharField()  # TEXTO, OPCION_MULTIPLE, ESCALA, etc.
    orden = IntegerField()
    opciones = JSONField()  # Para opciones múltiples

class Respuesta(models.Model):
    encuesta = ForeignKey(Encuesta)
    usuario = ForeignKey(User)
    pregunta = ForeignKey(Pregunta)
    respuesta = TextField()
    created_at = DateTimeField(auto_now_add=True)
```

### 5. Campos adicionales en User
```python
class User(AbstractUser):
    # ... campos existentes ...
    
    # Nuevos campos
    cv_file = FileField(upload_to='cvs/', null=True, blank=True)
    verificado = BooleanField(default=False)  # Para coordinador
    notificaciones_email = BooleanField(default=True)
    notificaciones_push = BooleanField(default=True)
```

### 6. Campos adicionales en Practica
```python
class Practica(models.Model):
    # ... campos existentes ...
    
    # Nuevos campos para proyecto
    descripcion_proyecto = TextField()
    objetivos = TextField()
    actividades_planificadas = TextField()
    competencias_desarrollar = TextField()
```

---

## 🚀 PLAN DE ACCIÓN INMEDIATO

¿Qué quieres implementar primero?

1. **Sistema de notificaciones** (más impacto en UX)
2. **Informes semanales del profesor** (core del sistema)
3. **Sistema de encuestas** (funcionalidad coordinador)
4. **Subir CV y verificar estudiantes** (quick wins)
5. **Forgot password** (funcionalidad estándar)

Dime cuál prefieres y empezamos 💪
