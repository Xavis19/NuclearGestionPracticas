"""
URLs para la app de vacantes.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EmpresaViewSet, VacanteViewSet

router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'', VacanteViewSet, basename='vacante')

app_name = 'vacantes'

urlpatterns = [
    path('', include(router.urls)),
]
