"""
Backend de autenticación personalizado que permite login con email O username
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Backend que permite autenticación con email o username
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autenticar con email o username
        """
        if username is None or password is None:
            return None
        
        try:
            # Intentar encontrar usuario por email O username
            user = User.objects.get(
                Q(email=username) | Q(username=username)
            )
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # Si hay múltiples usuarios, intentar con el email primero
            user = User.objects.filter(
                Q(email=username) | Q(username=username)
            ).first()
        
        # Verificar contraseña
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
