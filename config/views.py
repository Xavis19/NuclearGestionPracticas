"""
Vistas basadas en templates para el sistema de prácticas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from apps.usuarios.models import User
from apps.vacantes.models import Vacante, Empresa
from apps.practicas.models import Practica
from apps.postulaciones.models import Postulacion
from .forms import LoginForm, EstudianteForm, VacanteForm


def login_view(request):
    """Vista de login"""
    import logging
    logger = logging.getLogger('apps')
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        logger.debug(f"POST data: {request.POST}")
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            logger.info(f"Intento de login - Usuario: {username}")
            
            user = authenticate(request, username=username, password=password)
            logger.info(f"Resultado authenticate: {user}")
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.get_full_name() or user.username}!')
                return redirect('dashboard')
            else:
                logger.warning(f"Login fallido para usuario: {username}")
                messages.error(request, 'Credenciales inválidas')
        else:
            logger.error(f"Form no válido: {form.errors}")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Dashboard principal"""
    stats = {}
    
    if request.user.role == 'COORDINADOR':
        stats = {
            'total_estudiantes': User.objects.filter(role='ESTUDIANTE').count(),
            'total_vacantes': Vacante.objects.count(),
            'total_practicas': Practica.objects.filter(estado='EN_PROCESO').count(),
            'total_postulaciones': Postulacion.objects.count(),
        }
    elif request.user.role == 'PROFESOR':
        stats = {
            'estudiantes_asignados': 0,  # Implementar cuando tengamos la relación
            'practicas_supervisadas': 0,
        }
    elif request.user.role == 'ESTUDIANTE':
        stats = {
            'postulaciones': Postulacion.objects.filter(estudiante=request.user).count(),
            'practica_activa': Practica.objects.filter(
                estudiante=request.user,
                estado='EN_PROCESO'
            ).exists(),
        }
    
    return render(request, 'dashboard.html', {'stats': stats})


@login_required
def estudiantes_list(request):
    """Lista de estudiantes"""
    if request.user.role != 'COORDINADOR':
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('dashboard')
    
    estudiantes = User.objects.filter(role='ESTUDIANTE').order_by('-created_at')
    return render(request, 'estudiantes/list.html', {'estudiantes': estudiantes})


@login_required
def estudiante_create(request):
    """Crear estudiante"""
    if request.user.role != 'COORDINADOR':
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save(commit=False)
            estudiante.role = 'ESTUDIANTE'
            estudiante.set_password(form.cleaned_data['password1'])
            estudiante.save()
            messages.success(request, 'Estudiante creado correctamente')
            return redirect('estudiantes_list')
    else:
        form = EstudianteForm()
    
    return render(request, 'estudiantes/form.html', {'form': form})


@login_required
def estudiante_edit(request, pk):
    """Editar estudiante"""
    if request.user.role != 'COORDINADOR':
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('dashboard')
    
    estudiante = get_object_or_404(User, pk=pk, role='ESTUDIANTE')
    
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante, edit=True)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estudiante actualizado correctamente')
            return redirect('estudiantes_list')
    else:
        form = EstudianteForm(instance=estudiante, edit=True)
    
    return render(request, 'estudiantes/form.html', {'form': form})


@login_required
def estudiante_activate(request, pk):
    """Activar estudiante"""
    if request.user.role != 'COORDINADOR':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard')
    
    estudiante = get_object_or_404(User, pk=pk, role='ESTUDIANTE')
    estudiante.is_active = True
    estudiante.save()
    messages.success(request, f'Estudiante {estudiante.get_full_name()} activado')
    return redirect('estudiantes_list')


@login_required
def estudiante_deactivate(request, pk):
    """Desactivar estudiante"""
    if request.user.role != 'COORDINADOR':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard')
    
    estudiante = get_object_or_404(User, pk=pk, role='ESTUDIANTE')
    estudiante.is_active = False
    estudiante.save()
    messages.success(request, f'Estudiante {estudiante.get_full_name()} desactivado')
    return redirect('estudiantes_list')


@login_required
def vacantes_list(request):
    """Lista de vacantes"""
    if request.user.role != 'COORDINADOR':
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('dashboard')
    
    vacantes = Vacante.objects.select_related('empresa').order_by('-created_at')
    return render(request, 'vacantes/list.html', {'vacantes': vacantes})


@login_required
def vacante_create(request):
    """Crear vacante"""
    if request.user.role != 'COORDINADOR':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = VacanteForm(request.POST)
        if form.is_valid():
            vacante = form.save()
            messages.success(request, 'Vacante creada correctamente')
            return redirect('vacantes_list')
    else:
        form = VacanteForm()
    
    return render(request, 'vacantes/form.html', {'form': form})


@login_required
def vacante_edit(request, pk):
    """Editar vacante"""
    if request.user.role != 'COORDINADOR':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard')
    
    vacante = get_object_or_404(Vacante, pk=pk)
    
    if request.method == 'POST':
        form = VacanteForm(request.POST, instance=vacante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vacante actualizada correctamente')
            return redirect('vacantes_list')
    else:
        form = VacanteForm(instance=vacante)
    
    return render(request, 'vacantes/form.html', {'form': form})


@login_required
def vacante_publish(request, pk):
    """Publicar vacante"""
    if request.user.role != 'COORDINADOR':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard')
    
    vacante = get_object_or_404(Vacante, pk=pk)
    vacante.estado = 'ABIERTA'
    vacante.save()
    messages.success(request, f'Vacante "{vacante.titulo}" abierta')
    return redirect('vacantes_list')


@login_required
def vacante_close(request, pk):
    """Cerrar vacante"""
    if request.user.role != 'COORDINADOR':
        messages.error(request, 'No tienes permisos')
        return redirect('dashboard')
    
    vacante = get_object_or_404(Vacante, pk=pk)
    vacante.estado = 'CERRADA'
    vacante.save()
    messages.success(request, f'Vacante "{vacante.titulo}" cerrada')
    return redirect('vacantes_list')
