"""
URLs para la app de usuarios.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    EstudianteViewSet,
    ProfesorViewSet,
    CoordinadorViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'estudiantes', EstudianteViewSet, basename='estudiante')
router.register(r'profesores', ProfesorViewSet, basename='profesor')
router.register(r'coordinadores', CoordinadorViewSet, basename='coordinador')

app_name = 'usuarios'

urlpatterns = [
    path('', include(router.urls)),
]
