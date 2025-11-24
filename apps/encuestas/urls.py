from django.urls import path
from . import views

app_name = 'encuestas'

urlpatterns = [
    # Coordinadora - Gestión de encuestas
    path('crear/', views.crear_encuesta, name='crear'),
    path('lista/', views.lista_encuestas, name='lista'),
    path('resultados/<int:pk>/', views.resultados_encuesta, name='resultados'),
    path('publicar/<int:pk>/', views.publicar_encuesta, name='publicar'),
    path('cerrar/<int:pk>/', views.cerrar_encuesta, name='cerrar'),
    
    # Usuarios - Responder encuestas
    path('responder/<int:pk>/', views.responder_encuesta, name='responder'),
    path('mis-pendientes/', views.mis_encuestas_pendientes, name='mis_pendientes'),
    path('agradecimiento/', views.agradecimiento, name='agradecimiento'),
]
