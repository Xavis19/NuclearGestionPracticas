"""
Modelos para la app de vacantes.
RF-001: Gestión de Vacantes
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.usuarios.models import User


class Empresa(models.Model):
    """Modelo para Empresas."""
    
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    rfc = models.CharField(max_length=13, unique=True, verbose_name='RFC')
    razon_social = models.CharField(max_length=300, verbose_name='Razón Social')
    
    # Información de contacto
    direccion = models.TextField(verbose_name='Dirección')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    email = models.EmailField(verbose_name='Email')
    sitio_web = models.URLField(blank=True, null=True, verbose_name='Sitio Web')
    
    # Contacto principal
    contacto_nombre = models.CharField(max_length=200, verbose_name='Nombre del Contacto')
    contacto_puesto = models.CharField(max_length=100, verbose_name='Puesto del Contacto')
    contacto_email = models.EmailField(verbose_name='Email del Contacto')
    contacto_telefono = models.CharField(max_length=15, verbose_name='Teléfono del Contacto')
    
    # Información adicional
    sector = models.CharField(max_length=100, blank=True, null=True, verbose_name='Sector')
    tamaño = models.CharField(
        max_length=50,
        choices=[
            ('MICRO', 'Micro (1-10 empleados)'),
            ('PEQUEÑA', 'Pequeña (11-50 empleados)'),
            ('MEDIANA', 'Mediana (51-250 empleados)'),
            ('GRANDE', 'Grande (251+ empleados)'),
        ],
        blank=True,
        null=True,
        verbose_name='Tamaño'
    )
    
    # Estado
    activa = models.BooleanField(default=True, verbose_name='Activa')
    verificada = models.BooleanField(default=False, verbose_name='Verificada')
    
    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='empresas_creadas',
        verbose_name='Creado por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['rfc']),
            models.Index(fields=['nombre']),
            models.Index(fields=['activa']),
        ]
    
    def __str__(self):
        return self.nombre


class Vacante(models.Model):
    """
    Modelo para Vacantes de Prácticas.
    RF-001: Solo rol empresa/admin crea/edita.
    """
    
    # Estados
    ABIERTA = 'ABIERTA'
    CERRADA = 'CERRADA'
    PAUSADA = 'PAUSADA'
    CANCELADA = 'CANCELADA'
    
    ESTADO_CHOICES = [
        (ABIERTA, 'Abierta'),
        (CERRADA, 'Cerrada'),
        (PAUSADA, 'Pausada'),
        (CANCELADA, 'Cancelada'),
    ]
    
    # Información básica
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='vacantes',
        verbose_name='Empresa'
    )
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción')
    
    # Requisitos
    requisitos = models.TextField(verbose_name='Requisitos')
    carreras_solicitadas = models.CharField(
        max_length=500,
        help_text='Carreras separadas por comas',
        verbose_name='Carreras Solicitadas'
    )
    semestre_minimo = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Semestre Mínimo'
    )
    promedio_minimo = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        blank=True,
        null=True,
        verbose_name='Promedio Mínimo'
    )
    
    # Detalles de la práctica
    area = models.CharField(max_length=200, verbose_name='Área')
    modalidad = models.CharField(
        max_length=50,
        choices=[
            ('PRESENCIAL', 'Presencial'),
            ('REMOTO', 'Remoto'),
            ('HIBRIDO', 'Híbrido'),
        ],
        default='PRESENCIAL',
        verbose_name='Modalidad'
    )
    ubicacion = models.CharField(max_length=300, verbose_name='Ubicación')
    
    # Horario y duración
    horario = models.CharField(max_length=200, verbose_name='Horario')
    duracion_meses = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Duración (meses)'
    )
    
    # Cupos y fechas
    vacantes_disponibles = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name='Vacantes Disponibles'
    )
    vacantes_ocupadas = models.IntegerField(
        default=0,
        verbose_name='Vacantes Ocupadas'
    )
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_cierre_convocatoria = models.DateField(verbose_name='Fecha de Cierre de Convocatoria')
    
    # Beneficios (opcional)
    remunerada = models.BooleanField(default=False, verbose_name='Remunerada')
    monto_apoyo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Monto de Apoyo Mensual'
    )
    beneficios_adicionales = models.TextField(
        blank=True,
        null=True,
        verbose_name='Beneficios Adicionales'
    )
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ABIERTA,
        verbose_name='Estado'
    )
    
    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vacantes_creadas',
        verbose_name='Creado por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        verbose_name = 'Vacante'
        verbose_name_plural = 'Vacantes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['empresa', 'estado']),
            models.Index(fields=['estado', 'fecha_cierre_convocatoria']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.empresa.nombre}"
    
    @property
    def vacantes_restantes(self):
        """Calcular vacantes restantes."""
        return self.vacantes_disponibles - self.vacantes_ocupadas
    
    @property
    def esta_abierta(self):
        """Verificar si la vacante está abierta."""
        return self.estado == self.ABIERTA and self.vacantes_restantes > 0
    
    def puede_postularse(self, estudiante):
        """
        Verificar si un estudiante cumple los requisitos para postularse.
        """
        if not self.esta_abierta:
            return False, "La vacante no está disponible"
        
        # Verificar semestre
        if estudiante.semestre and estudiante.semestre < self.semestre_minimo:
            return False, f"Se requiere mínimo semestre {self.semestre_minimo}"
        
        # Verificar promedio
        if self.promedio_minimo and estudiante.promedio:
            if estudiante.promedio < self.promedio_minimo:
                return False, f"Se requiere promedio mínimo de {self.promedio_minimo}"
        
        # Verificar carrera
        if estudiante.carrera:
            carreras_lista = [c.strip().lower() for c in self.carreras_solicitadas.split(',')]
            if estudiante.carrera.lower() not in carreras_lista:
                return False, "Tu carrera no está en las solicitadas"
        
        return True, "Cumple los requisitos"
    
    def incrementar_ocupadas(self):
        """Incrementar contador de vacantes ocupadas."""
        self.vacantes_ocupadas += 1
        if self.vacantes_restantes == 0:
            self.estado = self.CERRADA
        self.save()
    
    def decrementar_ocupadas(self):
        """Decrementar contador de vacantes ocupadas."""
        if self.vacantes_ocupadas > 0:
            self.vacantes_ocupadas -= 1
            if self.estado == self.CERRADA and self.vacantes_restantes > 0:
                self.estado = self.ABIERTA
            self.save()
