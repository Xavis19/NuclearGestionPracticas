from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from apps.usuarios.decorators import role_required
from apps.practicas.models import Practica
from apps.entregables.models import Entregable


@login_required
@role_required(['TUTOR_EMPRESARIAL'])
def dashboard_tutor(request):
    """Dashboard principal del Tutor Empresarial"""
    tutor = request.user
    
    # Obtener prácticas donde este usuario es tutor
    practicas_activas_lista = Practica.objects.filter(
        tutor_empresarial=tutor,
        estado__in=['EN_PROCESO', 'INICIADA']
    )
    
    # Estadísticas generales
    total_estudiantes = practicas_activas_lista.values('estudiante').distinct().count()
    practicas_activas = practicas_activas_lista.count()
    
    # Entregables pendientes de evaluación
    entregables_pendientes_lista = Entregable.objects.filter(
        practica__tutor_empresarial=tutor,
        estado='PENDIENTE'
    ).order_by('fecha_limite')[:5]
    
    entregables_pendientes = entregables_pendientes_lista.count()
    
    # Calcular promedio general de calificaciones
    promedio_general = Entregable.objects.filter(
        practica__tutor_empresarial=tutor,
        calificacion__isnull=False
    ).aggregate(Avg('calificacion'))['calificacion__avg'] or 0
    
    # Actividad reciente (últimas 10 actividades)
    actividades_recientes = []
    entregables_recientes = Entregable.objects.filter(
        practica__tutor_empresarial=tutor
    ).order_by('-fecha_entrega')[:10]
    
    for entregable in entregables_recientes:
        actividades_recientes.append({
            'fecha': entregable.fecha_entrega,
            'descripcion': f"{entregable.practica.estudiante.get_full_name()} entregó '{entregable.titulo}'"
        })
    
    context = {
        'total_estudiantes': total_estudiantes,
        'entregables_pendientes': entregables_pendientes,
        'promedio_general': promedio_general,
        'practicas_activas': practicas_activas,
        'entregables_pendientes_lista': entregables_pendientes_lista,
        'practicas_activas_lista': practicas_activas_lista[:5],
        'actividades_recientes': actividades_recientes,
    }
    
    return render(request, 'tutores/dashboard.html', context)


@login_required
@role_required(['TUTOR_EMPRESARIAL'])
def estudiantes_lista(request):
    """Lista de estudiantes asignados al tutor"""
    tutor = request.user
    practicas = Practica.objects.filter(tutor_empresarial=tutor)
    
    context = {
        'practicas': practicas,
    }
    
    return render(request, 'tutores/estudiantes.html', context)


@login_required
@role_required(['TUTOR_EMPRESARIAL'])
def progreso_general(request):
    """Vista de progreso general de estudiantes"""
    tutor = request.user
    practicas = Practica.objects.filter(tutor_empresarial=tutor)
    
    # Calcular estadísticas por estudiante
    estadisticas = []
    for practica in practicas:
        total_entregables = practica.entregables.count()
        evaluados = practica.entregables.filter(calificacion__isnull=False).count()
        promedio = practica.entregables.filter(
            calificacion__isnull=False
        ).aggregate(Avg('calificacion'))['calificacion__avg'] or 0
        
        estadisticas.append({
            'practica': practica,
            'total_entregables': total_entregables,
            'evaluados': evaluados,
            'promedio': promedio,
        })
    
    context = {
        'estadisticas': estadisticas,
    }
    
    return render(request, 'tutores/progreso.html', context)
