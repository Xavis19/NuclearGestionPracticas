from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    """
    Decorador para verificar que el usuario tenga uno de los roles permitidos
    
    Uso:
        @role_required(['ESTUDIANTE'])
        def mi_vista(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión')
                return redirect('usuarios:login')
            
            # Verificar si el usuario tiene uno de los roles permitidos
            if request.user.role in allowed_roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Si no tiene permiso, mostrar mensaje y redirigir
            messages.error(request, 'No tienes permiso para acceder a esta página')
            return redirect('config:dashboard')
        
        return wrapper
    return decorator
