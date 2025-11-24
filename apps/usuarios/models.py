"""
Modelos para la app de usuarios.
RF-011: Autenticación y Roles
RF-012: Registro de Estudiantes
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError('El usuario debe tener un email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.COORDINADORA_EMPRESARIAL)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model con roles.
    Roles: ESTUDIANTE, DOCENTE_ASESOR, TUTOR_EMPRESARIAL, COORDINADORA_EMPRESARIAL
    """
    
    # Roles
    ESTUDIANTE = 'ESTUDIANTE'
    DOCENTE_ASESOR = 'DOCENTE_ASESOR'
    TUTOR_EMPRESARIAL = 'TUTOR_EMPRESARIAL'
    COORDINADORA_EMPRESARIAL = 'COORDINADORA_EMPRESARIAL'
    
    ROLE_CHOICES = [
        (ESTUDIANTE, 'Estudiante'),
        (DOCENTE_ASESOR, 'Docente Asesor'),
        (TUTOR_EMPRESARIAL, 'Tutor Empresarial'),
        (COORDINADORA_EMPRESARIAL, 'Coordinadora Empresarial'),
    ]
    
    # Validators
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos."
    )
    
    # Fields
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default=ESTUDIANTE,
        verbose_name='Rol'
    )
    
    # Información personal
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    
    # Para estudiantes
    matricula = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Matrícula'
    )
    carrera = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Carrera'
    )
    semestre = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Semestre'
    )
    promedio = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Promedio'
    )
    
    # Para docentes asesores
    departamento = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Departamento'
    )
    especialidad = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Especialidad'
    )
    
    # Para tutores empresariales (se relacionarán con Empresa)
    empresa = models.ForeignKey(
        'vacantes.Empresa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tutores_empresariales',
        verbose_name='Empresa',
        help_text='Empresa a la que pertenece el tutor empresarial'
    )
    puesto = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Puesto',
        help_text='Cargo del tutor en la empresa'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['matricula']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Return the full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_coordinadora(self):
        """Check if user is coordinadora empresarial."""
        return self.role == self.COORDINADORA_EMPRESARIAL
    
    @property
    def is_docente_asesor(self):
        """Check if user is docente asesor."""
        return self.role == self.DOCENTE_ASESOR
    
    @property
    def is_tutor_empresarial(self):
        """Check if user is tutor empresarial."""
        return self.role == self.TUTOR_EMPRESARIAL
    
    @property
    def is_estudiante(self):
        """Check if user is student."""
        return self.role == self.ESTUDIANTE
    
    def save(self, *args, **kwargs):
        """Override save to validate role-specific fields."""
        # Validar que estudiantes tengan matrícula
        if self.role == self.ESTUDIANTE and not self.matricula:
            # Si no tiene matrícula, generarla automáticamente
            from django.utils.crypto import get_random_string
            self.matricula = f"EST{get_random_string(8, allowed_chars='0123456789')}"
        
        # Limpiar campos según rol
        if self.role != self.ESTUDIANTE:
            self.matricula = None
            self.carrera = None
            self.semestre = None
            self.promedio = None
        
        if self.role != self.DOCENTE_ASESOR:
            self.departamento = None
            self.especialidad = None
        
        if self.role != self.TUTOR_EMPRESARIAL:
            self.empresa = None
            self.puesto = None
        
        super().save(*args, **kwargs)
