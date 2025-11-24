"""
Modelos para el sistema de encuestas.
Sistema para crear encuestas y recopilar retroalimentación de estudiantes, tutores y coordinadora.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.usuarios.models import User
from apps.practicas.models import Practica


class Encuesta(models.Model):
    """
    Modelo para encuestas del sistema.
    La coordinadora crea encuestas dirigidas a diferentes roles.
    """
    
    # Tipos de destinatarios
    ESTUDIANTES = 'ESTUDIANTES'
    TUTORES = 'TUTORES'
    DOCENTES = 'DOCENTES'
    TODOS = 'TODOS'
    
    DESTINATARIO_CHOICES = [
        (ESTUDIANTES, 'Estudiantes'),
        (TUTORES, 'Tutores Empresariales'),
        (DOCENTES, 'Docentes Asesores'),
        (TODOS, 'Todos los usuarios'),
    ]
    
    # Estados
    BORRADOR = 'BORRADOR'
    ACTIVA = 'ACTIVA'
    CERRADA = 'CERRADA'
    
    ESTADO_CHOICES = [
        (BORRADOR, 'Borrador'),
        (ACTIVA, 'Activa'),
        (CERRADA, 'Cerrada'),
    ]
    
    # Campos básicos
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción', blank=True)
    
    # Destinatarios
    dirigida_a = models.CharField(
        max_length=20,
        choices=DESTINATARIO_CHOICES,
        default=ESTUDIANTES,
        verbose_name='Dirigida a'
    )
    
    # Estado y fechas
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default=BORRADOR,
        verbose_name='Estado'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_inicio = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de inicio')
    fecha_cierre = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de cierre')
    
    # Creador
    creada_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='encuestas_creadas',
        verbose_name='Creada por'
    )
    
    # Opciones
    es_anonima = models.BooleanField(default=False, verbose_name='Es anónima')
    permite_multiple = models.BooleanField(
        default=False,
        verbose_name='Permitir responder múltiples veces'
    )
    
    class Meta:
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.get_dirigida_a_display()}"
    
    def total_respuestas(self):
        """Total de respuestas recibidas"""
        return self.respuestas.count()
    
    def tasa_respuesta(self):
        """Calcula la tasa de respuesta basada en los usuarios objetivo"""
        if self.dirigida_a == self.ESTUDIANTES:
            total_usuarios = User.objects.filter(role=User.ESTUDIANTE).count()
        elif self.dirigida_a == self.TUTORES:
            total_usuarios = User.objects.filter(role=User.TUTOR_EMPRESARIAL).count()
        elif self.dirigida_a == self.DOCENTES:
            total_usuarios = User.objects.filter(role=User.DOCENTE_ASESOR).count()
        else:
            total_usuarios = User.objects.exclude(is_superuser=True).count()
        
        if total_usuarios == 0:
            return 0
        
        respuestas = self.respuestas.values('usuario').distinct().count()
        return (respuestas / total_usuarios) * 100


class Pregunta(models.Model):
    """
    Modelo para las preguntas de una encuesta.
    """
    
    # Tipos de pregunta
    TEXTO_CORTO = 'TEXTO_CORTO'
    TEXTO_LARGO = 'TEXTO_LARGO'
    OPCION_MULTIPLE = 'OPCION_MULTIPLE'
    SELECCION_UNICA = 'SELECCION_UNICA'
    ESCALA = 'ESCALA'
    SI_NO = 'SI_NO'
    
    TIPO_CHOICES = [
        (TEXTO_CORTO, 'Texto Corto'),
        (TEXTO_LARGO, 'Texto Largo'),
        (OPCION_MULTIPLE, 'Opción Múltiple'),
        (SELECCION_UNICA, 'Selección Única'),
        (ESCALA, 'Escala (1-5)'),
        (SI_NO, 'Sí/No'),
    ]
    
    # Relaciones
    encuesta = models.ForeignKey(
        Encuesta,
        on_delete=models.CASCADE,
        related_name='preguntas',
        verbose_name='Encuesta'
    )
    
    # Campos
    texto = models.TextField(verbose_name='Texto de la pregunta')
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default=TEXTO_CORTO,
        verbose_name='Tipo de pregunta'
    )
    orden = models.PositiveIntegerField(default=0, verbose_name='Orden')
    es_requerida = models.BooleanField(default=True, verbose_name='Es requerida')
    
    # Para preguntas con opciones (OPCION_MULTIPLE o SELECCION_UNICA)
    opciones = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Opciones',
        help_text='Lista de opciones para preguntas de selección'
    )
    
    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['encuesta', 'orden']
        unique_together = ['encuesta', 'orden']
    
    def __str__(self):
        return f"{self.encuesta.titulo} - {self.texto[:50]}"


class RespuestaEncuesta(models.Model):
    """
    Modelo para las respuestas a encuestas.
    """
    
    # Relaciones
    encuesta = models.ForeignKey(
        Encuesta,
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name='Encuesta'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='respuestas_encuestas',
        verbose_name='Usuario'
    )
    practica = models.ForeignKey(
        Practica,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='respuestas_encuestas',
        verbose_name='Práctica relacionada'
    )
    
    # Campos
    fecha_respuesta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de respuesta')
    
    class Meta:
        verbose_name = 'Respuesta de Encuesta'
        verbose_name_plural = 'Respuestas de Encuestas'
        ordering = ['-fecha_respuesta']
    
    def __str__(self):
        usuario_str = self.usuario.get_full_name() if self.usuario else 'Anónimo'
        return f"{self.encuesta.titulo} - {usuario_str}"


class DetallePregunta(models.Model):
    """
    Modelo para el detalle de cada respuesta a una pregunta específica.
    """
    
    # Relaciones
    respuesta_encuesta = models.ForeignKey(
        RespuestaEncuesta,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Respuesta de encuesta'
    )
    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name='Pregunta'
    )
    
    # Campos de respuesta
    respuesta_texto = models.TextField(null=True, blank=True, verbose_name='Respuesta de texto')
    respuesta_numerica = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Respuesta numérica'
    )
    respuesta_booleana = models.BooleanField(null=True, blank=True, verbose_name='Respuesta Sí/No')
    opciones_seleccionadas = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Opciones seleccionadas'
    )
    
    class Meta:
        verbose_name = 'Detalle de Respuesta'
        verbose_name_plural = 'Detalles de Respuestas'
        unique_together = ['respuesta_encuesta', 'pregunta']
    
    def __str__(self):
        return f"{self.pregunta.texto[:30]} - {self.respuesta_encuesta.usuario}"