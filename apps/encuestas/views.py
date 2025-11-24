"""
Vistas para el sistema de encuestas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg
from apps.usuarios.decorators import role_required
from .models import Encuesta, Pregunta, RespuestaEncuesta, DetallePregunta


@login_required
@role_required(['COORDINADORA_EMPRESARIAL'])
def crear_encuesta(request):
    """Vista para crear una nueva encuesta"""
    if request.method == 'POST':
        # Crear encuesta
        encuesta = Encuesta.objects.create(
            titulo=request.POST.get('titulo'),
            descripcion=request.POST.get('descripcion'),
            dirigida_a=request.POST.get('dirigida_a'),
            es_anonima=request.POST.get('es_anonima') == 'on',
            creada_por=request.user,
            estado=Encuesta.BORRADOR
        )
        
        # Crear preguntas
        num_preguntas = int(request.POST.get('num_preguntas', 0))
        for i in range(num_preguntas):
            texto = request.POST.get(f'pregunta_{i}_texto')
            tipo = request.POST.get(f'pregunta_{i}_tipo')
            es_requerida = request.POST.get(f'pregunta_{i}_requerida') == 'on'
            
            if texto:
                pregunta = Pregunta.objects.create(
                    encuesta=encuesta,
                    texto=texto,
                    tipo=tipo,
                    orden=i,
                    es_requerida=es_requerida
                )
                
                # Si es pregunta con opciones, guardar las opciones
                if tipo in [Pregunta.OPCION_MULTIPLE, Pregunta.SELECCION_UNICA]:
                    opciones = request.POST.get(f'pregunta_{i}_opciones', '').split('\n')
                    pregunta.opciones = [op.strip() for op in opciones if op.strip()]
                    pregunta.save()
        
        messages.success(request, 'Encuesta creada correctamente')
        return redirect('encuestas:detalle', pk=encuesta.pk)
    
    return render(request, 'encuestas/crear.html')


@login_required
@role_required(['COORDINADORA_EMPRESARIAL'])
def lista_encuestas(request):
    """Lista de todas las encuestas"""
    encuestas = Encuesta.objects.all().annotate(
        total_respuestas=Count('respuestas')
    )
    
    context = {
        'encuestas': encuestas,
    }
    return render(request, 'encuestas/lista.html', context)


@login_required
def responder_encuesta(request, pk):
    """Vista para responder una encuesta"""
    encuesta = get_object_or_404(Encuesta, pk=pk, estado=Encuesta.ACTIVA)
    
    # Verificar si el usuario puede responder esta encuesta
    if encuesta.dirigida_a == Encuesta.ESTUDIANTES and request.user.role != 'ESTUDIANTE':
        messages.error(request, 'Esta encuesta no está dirigida a tu rol')
        return redirect('config:dashboard')
    
    if encuesta.dirigida_a == Encuesta.TUTORES and request.user.role != 'TUTOR_EMPRESARIAL':
        messages.error(request, 'Esta encuesta no está dirigida a tu rol')
        return redirect('config:dashboard')
    
    # Verificar si ya respondió
    if not encuesta.permite_multiple:
        ya_respondio = RespuestaEncuesta.objects.filter(
            encuesta=encuesta,
            usuario=request.user
        ).exists()
        
        if ya_respondio:
            messages.info(request, 'Ya has respondido esta encuesta')
            return redirect('encuestas:agradecimiento')
    
    if request.method == 'POST':
        # Crear respuesta
        respuesta = RespuestaEncuesta.objects.create(
            encuesta=encuesta,
            usuario=request.user if not encuesta.es_anonima else None
        )
        
        # Guardar respuestas a cada pregunta
        for pregunta in encuesta.preguntas.all():
            clave = f'pregunta_{pregunta.id}'
            
            if pregunta.tipo == Pregunta.TEXTO_CORTO or pregunta.tipo == Pregunta.TEXTO_LARGO:
                respuesta_texto = request.POST.get(clave)
                if respuesta_texto or not pregunta.es_requerida:
                    DetallePregunta.objects.create(
                        respuesta_encuesta=respuesta,
                        pregunta=pregunta,
                        respuesta_texto=respuesta_texto
                    )
            
            elif pregunta.tipo == Pregunta.ESCALA:
                respuesta_numerica = request.POST.get(clave)
                if respuesta_numerica:
                    DetallePregunta.objects.create(
                        respuesta_encuesta=respuesta,
                        pregunta=pregunta,
                        respuesta_numerica=int(respuesta_numerica)
                    )
            
            elif pregunta.tipo == Pregunta.SI_NO:
                respuesta_booleana = request.POST.get(clave)
                if respuesta_booleana:
                    DetallePregunta.objects.create(
                        respuesta_encuesta=respuesta,
                        pregunta=pregunta,
                        respuesta_booleana=respuesta_booleana == 'si'
                    )
            
            elif pregunta.tipo in [Pregunta.OPCION_MULTIPLE, Pregunta.SELECCION_UNICA]:
                if pregunta.tipo == Pregunta.OPCION_MULTIPLE:
                    opciones = request.POST.getlist(clave)
                else:
                    opciones = [request.POST.get(clave)]
                
                if opciones and opciones[0]:
                    DetallePregunta.objects.create(
                        respuesta_encuesta=respuesta,
                        pregunta=pregunta,
                        opciones_seleccionadas=opciones
                    )
        
        messages.success(request, '¡Gracias por responder la encuesta!')
        return redirect('encuestas:agradecimiento')
    
    context = {
        'encuesta': encuesta,
        'preguntas': encuesta.preguntas.all().order_by('orden'),
    }
    return render(request, 'encuestas/responder.html', context)


@login_required
def agradecimiento(request):
    """Página de agradecimiento después de responder"""
    return render(request, 'encuestas/agradecimiento.html')


@login_required
@role_required(['COORDINADORA_EMPRESARIAL'])
def resultados_encuesta(request, pk):
    """Vista de resultados de una encuesta"""
    encuesta = get_object_or_404(Encuesta, pk=pk)
    
    # Obtener estadísticas
    total_respuestas = encuesta.respuestas.count()
    tasa_respuesta = encuesta.tasa_respuesta()
    
    # Resultados por pregunta
    resultados = []
    for pregunta in encuesta.preguntas.all().order_by('orden'):
        detalles = DetallePregunta.objects.filter(pregunta=pregunta)
        
        if pregunta.tipo == Pregunta.ESCALA:
            promedio = detalles.aggregate(Avg('respuesta_numerica'))['respuesta_numerica__avg']
            distribucion = {}
            for i in range(1, 6):
                distribucion[i] = detalles.filter(respuesta_numerica=i).count()
            
            resultados.append({
                'pregunta': pregunta,
                'tipo': 'escala',
                'promedio': round(promedio, 2) if promedio else 0,
                'distribucion': distribucion,
            })
        
        elif pregunta.tipo in [Pregunta.OPCION_MULTIPLE, Pregunta.SELECCION_UNICA]:
            respuestas = {}
            for detalle in detalles:
                for opcion in detalle.opciones_seleccionadas:
                    respuestas[opcion] = respuestas.get(opcion, 0) + 1
            
            resultados.append({
                'pregunta': pregunta,
                'tipo': 'opciones',
                'respuestas': respuestas,
            })
        
        elif pregunta.tipo == Pregunta.SI_NO:
            si_count = detalles.filter(respuesta_booleana=True).count()
            no_count = detalles.filter(respuesta_booleana=False).count()
            
            resultados.append({
                'pregunta': pregunta,
                'tipo': 'si_no',
                'si': si_count,
                'no': no_count,
            })
        
        else:  # Texto
            respuestas_texto = detalles.values_list('respuesta_texto', flat=True)
            resultados.append({
                'pregunta': pregunta,
                'tipo': 'texto',
                'respuestas': list(respuestas_texto),
            })
    
    context = {
        'encuesta': encuesta,
        'total_respuestas': total_respuestas,
        'tasa_respuesta': round(tasa_respuesta, 1),
        'resultados': resultados,
    }
    
    return render(request, 'encuestas/resultados.html', context)


@login_required
@role_required(['COORDINADORA_EMPRESARIAL'])
def publicar_encuesta(request, pk):
    """Publicar una encuesta (cambiar de BORRADOR a ACTIVA)"""
    encuesta = get_object_or_404(Encuesta, pk=pk)
    encuesta.estado = Encuesta.ACTIVA
    encuesta.fecha_inicio = timezone.now()
    encuesta.save()
    
    messages.success(request, f'Encuesta "{encuesta.titulo}" publicada correctamente')
    return redirect('encuestas:lista')


@login_required
@role_required(['COORDINADORA_EMPRESARIAL'])
def cerrar_encuesta(request, pk):
    """Cerrar una encuesta"""
    encuesta = get_object_or_404(Encuesta, pk=pk)
    encuesta.estado = Encuesta.CERRADA
    encuesta.fecha_cierre = timezone.now()
    encuesta.save()
    
    messages.success(request, f'Encuesta "{encuesta.titulo}" cerrada')
    return redirect('encuestas:resultados', pk=pk)


@login_required
def mis_encuestas_pendientes(request):
    """Lista de encuestas pendientes de responder para el usuario actual"""
    # Filtrar encuestas según el rol
    if request.user.role == 'ESTUDIANTE':
        dirigida = [Encuesta.ESTUDIANTES, Encuesta.TODOS]
    elif request.user.role == 'TUTOR_EMPRESARIAL':
        dirigida = [Encuesta.TUTORES, Encuesta.TODOS]
    elif request.user.role == 'DOCENTE_ASESOR':
        dirigida = [Encuesta.DOCENTES, Encuesta.TODOS]
    else:
        dirigida = []
    
    # Obtener encuestas activas
    encuestas_disponibles = Encuesta.objects.filter(
        estado=Encuesta.ACTIVA,
        dirigida_a__in=dirigida
    )
    
    # Filtrar las que ya respondió
    encuestas_pendientes = []
    for encuesta in encuestas_disponibles:
        ya_respondio = RespuestaEncuesta.objects.filter(
            encuesta=encuesta,
            usuario=request.user
        ).exists()
        
        if not ya_respondio or encuesta.permite_multiple:
            encuestas_pendientes.append(encuesta)
    
    context = {
        'encuestas': encuestas_pendientes,
    }
    
    return render(request, 'encuestas/mis_pendientes.html', context)
