"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from apps.usuarios.auth_views import CustomTokenObtainPairView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Template-based views
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Estudiantes
    path('estudiantes/', views.estudiantes_list, name='estudiantes_list'),
    path('estudiantes/crear/', views.estudiante_create, name='estudiante_create'),
    path('estudiantes/<int:pk>/editar/', views.estudiante_edit, name='estudiante_edit'),
    path('estudiantes/<int:pk>/activar/', views.estudiante_activate, name='estudiante_activate'),
    path('estudiantes/<int:pk>/desactivar/', views.estudiante_deactivate, name='estudiante_deactivate'),
    
    # Vacantes
    path('vacantes/', views.vacantes_list, name='vacantes_list'),
    path('vacantes/crear/', views.vacante_create, name='vacante_create'),
    path('vacantes/<int:pk>/editar/', views.vacante_edit, name='vacante_edit'),
    path('vacantes/<int:pk>/publicar/', views.vacante_publish, name='vacante_publish'),
    path('vacantes/<int:pk>/cerrar/', views.vacante_close, name='vacante_close'),
    
    # JWT Authentication endpoints (para API)
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # App URLs (API)
    path('api/usuarios/', include('apps.usuarios.urls')),
    path('api/vacantes/', include('apps.vacantes.urls')),
    path('api/postulaciones/', include('apps.postulaciones.urls')),
    path('api/documentos/', include('apps.documentos.urls')),
    path('api/contratos/', include('apps.contratos.urls')),
    path('api/tutores/', include('apps.tutores.urls')),
    path('api/encuestas/', include('apps.encuestas.urls')),
    path('api/reportes/', include('apps.reportes.urls')),
    path('api/seguimiento/', include('apps.seguimiento.urls')),
    path('api/evaluaciones/', include('apps.evaluaciones.urls')),
    path('api/cierre/', include('apps.cierre.urls')),
    path('api/practicas/', include('apps.practicas.urls')),
    path('api/observaciones/', include('apps.observaciones.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Sistema de Gestión de Prácticas"
admin.site.site_title = "Admin Prácticas"
admin.site.index_title = "Administración del Sistema"
