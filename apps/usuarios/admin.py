"""
Admin para la app de usuarios.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para User."""
    
    list_display = [
        'email', 'username', 'first_name', 'last_name',
        'role', 'is_active', 'is_staff', 'created_at'
    ]
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'matricula']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Información Personal'), {
            'fields': ('first_name', 'last_name', 'phone')
        }),
        (_('Rol y Permisos'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Información de Estudiante'), {
            'fields': ('matricula', 'carrera', 'semestre', 'promedio'),
            'classes': ('collapse',),
        }),
        (_('Información de Profesor'), {
            'fields': ('departamento', 'especialidad'),
            'classes': ('collapse',),
        }),
        (_('Fechas Importantes'), {
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'role', 'is_staff', 'is_active'
            ),
        }),
    )
    
    def get_queryset(self, request):
        """Personalizar queryset."""
        qs = super().get_queryset(request)
        return qs.select_related()
