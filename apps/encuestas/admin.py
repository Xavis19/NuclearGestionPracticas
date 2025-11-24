from django.contrib import admin
from .models import Encuesta, Pregunta, RespuestaEncuesta, DetallePregunta


class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1
    fields = ['texto', 'tipo', 'orden', 'es_requerida', 'opciones']


@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'dirigida_a', 'estado', 'fecha_creacion', 'total_respuestas']
    list_filter = ['dirigida_a', 'estado', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    inlines = [PreguntaInline]
    
    def total_respuestas(self, obj):
        return obj.respuestas.count()
    total_respuestas.short_description = 'Respuestas'


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['encuesta', 'texto', 'tipo', 'orden', 'es_requerida']
    list_filter = ['tipo', 'es_requerida']
    search_fields = ['texto']


@admin.register(RespuestaEncuesta)
class RespuestaEncuestaAdmin(admin.ModelAdmin):
    list_display = ['encuesta', 'usuario', 'fecha_respuesta']
    list_filter = ['fecha_respuesta']
    search_fields = ['usuario__email', 'usuario__first_name', 'usuario__last_name']


@admin.register(DetallePregunta)
class DetallePreguntaAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta_encuesta', 'respuesta_texto']
    list_filter = ['pregunta__tipo']
