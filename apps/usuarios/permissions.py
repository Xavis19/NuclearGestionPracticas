"""
Permisos personalizados para la app de usuarios.
"""

from rest_framework import permissions


class IsCoordinador(permissions.BasePermission):
    """Permiso para coordinadores."""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_coordinador
        )


class IsProfesor(permissions.BasePermission):
    """Permiso para profesores."""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_profesor
        )


class IsEstudiante(permissions.BasePermission):
    """Permiso para estudiantes."""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_estudiante
        )


class IsCoordinadorOrProfesor(permissions.BasePermission):
    """Permiso para coordinadores o profesores."""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.is_coordinador or request.user.is_profesor)
        )


class IsOwnerOrCoordinador(permissions.BasePermission):
    """
    Permiso para el dueño del objeto o coordinador.
    El objeto debe tener un atributo 'user' o 'estudiante'.
    """
    
    def has_object_permission(self, request, view, obj):
        # Coordinadores tienen acceso total
        if request.user.is_coordinador:
            return True
        
        # Verificar si el usuario es el dueño
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'estudiante'):
            return obj.estudiante == request.user
        
        return False


class IsReadOnlyOrCoordinador(permissions.BasePermission):
    """
    Permiso de solo lectura para todos,
    pero escritura solo para coordinadores.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_coordinador
        )
