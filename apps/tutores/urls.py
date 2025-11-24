from django.urls import path
from . import views

app_name = 'tutores'

urlpatterns = [
    path('dashboard/', views.dashboard_tutor, name='dashboard'),
    path('estudiantes/', views.estudiantes_lista, name='estudiantes'),
    path('progreso/', views.progreso_general, name='progreso'),
]
