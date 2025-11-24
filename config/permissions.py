"""
Permisos personalizados para el sistema de gestión de prácticas.
Define los permisos de acceso según el rol del usuario.
"""

from rest_framework import permissions


class IsCoordinadora(permissions.BasePermission):
    """Permiso para coordinadora empresarial."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_coordinadora


class IsDocenteAsesor(permissions.BasePermission):
    """Permiso para docente asesor."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_docente_asesor


class IsTutorEmpresarial(permissions.BasePermission):
    """Permiso para tutor empresarial."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_tutor_empresarial


class IsEstudiante(permissions.BasePermission):
    """Permiso para estudiante."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_estudiante


class IsCoordinadoraOrReadOnly(permissions.BasePermission):
    """
    Permiso para coordinadora (puede crear/editar).
    Otros roles solo lectura.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_coordinadora


class CannotModifyGrades(permissions.BasePermission):
    """
    Permiso que previene modificar calificaciones.
    Solo tutores empresariales pueden modificar calificaciones.
    Coordinadora puede verlas pero no modificarlas.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Si es una acción de modificación de calificaciones
        if view.action in ['update', 'partial_update', 'destroy']:
            # Solo tutor empresarial puede modificar calificaciones en entregables
            if view.basename == 'entregable':
                return request.user.is_tutor_empresarial
        
        return True
    
    def has_object_permission(self, request, view, obj):
        # Coordinadora no puede modificar calificaciones
        if request.user.is_coordinadora:
            if request.method in ['PUT', 'PATCH'] and hasattr(obj, 'calificacion'):
                # Verificar si se está intentando modificar la calificación
                if 'calificacion' in request.data:
                    return False
        return True


class PracticaPermissions(permissions.BasePermission):
    """
    Permisos específicos para Prácticas:
    - Coordinadora: puede crear, asignar, cerrar
    - Docente Asesor: puede ver y hacer seguimiento de sus prácticas
    - Tutor Empresarial: puede ver prácticas de su empresa
    - Estudiante: puede ver su práctica
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Solo coordinadora puede crear/asignar prácticas
        if view.action in ['create', 'asignar', 'cerrar']:
            return request.user.is_coordinadora
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Todos pueden ver sus prácticas relacionadas
            if request.user.is_estudiante:
                return obj.estudiante == request.user
            elif request.user.is_docente_asesor:
                return obj.docente_asesor == request.user
            elif request.user.is_tutor_empresarial:
                return obj.tutor_empresarial == request.user
            elif request.user.is_coordinadora:
                return True
        
        # Solo coordinadora puede modificar
        return request.user.is_coordinadora


class EntregablePermissions(permissions.BasePermission):
    """
    Permisos específicos para Entregables:
    - Estudiante: puede crear y enviar sus entregables
    - Tutor Empresarial: puede evaluar entregables
    - Docente Asesor: puede ver entregables
    - Coordinadora: puede ver todos los entregables
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if view.action == 'create':
            return request.user.is_estudiante
        
        if view.action == 'evaluar':
            return request.user.is_tutor_empresarial
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if view.action == 'evaluar':
            # Solo el tutor empresarial de la práctica puede evaluar
            return request.user.is_tutor_empresarial and obj.practica.tutor_empresarial == request.user
        
        if view.action in ['update', 'partial_update', 'destroy']:
            # Solo el estudiante dueño puede modificar (antes de enviar)
            return request.user.is_estudiante and obj.estudiante == request.user
        
        # Para lectura, verificar relación
        if request.user.is_estudiante:
            return obj.estudiante == request.user
        elif request.user.is_docente_asesor:
            return obj.practica.docente_asesor == request.user
        elif request.user.is_tutor_empresarial:
            return obj.practica.tutor_empresarial == request.user
        elif request.user.is_coordinadora:
            return True
        
        return False


class ReunionPermissions(permissions.BasePermission):
    """
    Permisos específicos para Reuniones:
    - Docente Asesor: puede crear, modificar y gestionar reuniones
    - Estudiante: puede ver sus reuniones
    - Coordinadora: puede ver todas las reuniones
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if view.action == 'create':
            return request.user.is_docente_asesor
        
        if view.action in ['marcar_realizada', 'reprogramar', 'cancelar']:
            return request.user.is_docente_asesor
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy', 'marcar_realizada', 'reprogramar', 'cancelar']:
            # Solo el docente asesor dueño puede modificar
            return request.user.is_docente_asesor and obj.docente_asesor == request.user
        
        # Para lectura
        if request.user.is_estudiante:
            return obj.estudiante == request.user
        elif request.user.is_docente_asesor:
            return obj.docente_asesor == request.user
        elif request.user.is_coordinadora:
            return True
        
        return False


class NotificacionPermissions(permissions.BasePermission):
    """
    Permisos específicos para Notificaciones:
    - Coordinadora: puede crear y enviar notificaciones
    - Estudiante: puede ver y marcar como leídas sus notificaciones
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if view.action in ['create', 'enviar']:
            return request.user.is_coordinadora
        
        if view.action in ['marcar_leida', 'confirmar', 'no_leidas']:
            return request.user.is_estudiante
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_coordinadora and obj.remitente == request.user
        
        if view.action in ['marcar_leida', 'confirmar']:
            return request.user.is_estudiante and obj.destinatario == request.user
        
        # Para lectura
        if request.user.is_estudiante:
            return obj.destinatario == request.user
        elif request.user.is_coordinadora:
            return True
        
        return False
