
from django.contrib import admin

from .models import (
    Evaluacion,
    Pregunta,
    OpcionRespuesta,
    IntentoEvaluacion,
    RespuestaEstudiante,
)


class OpcionRespuestaInline(admin.TabularInline):
    model = OpcionRespuesta
    extra = 2


class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1
    fields = (
        "enunciado",
        "tema",
        "orden",
        "puntaje",
        "es_provisional",
        "activa",
    )
    show_change_link = True


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "materia",
        "activa",
        "fecha_creacion",
    )
    list_filter = ("materia", "activa")
    search_fields = ("titulo", "descripcion")
    inlines = [PreguntaInline]


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = (
        "enunciado_resumido",
        "evaluacion",
        "tema",
        "orden",
        "puntaje",
        "es_provisional",
        "activa",
    )
    list_filter = (
        "evaluacion__materia",
        "es_provisional",
        "activa",
    )
    search_fields = ("enunciado", "evaluacion__titulo")
    filter_horizontal = ("habilidades",)
    inlines = [OpcionRespuestaInline]

    @admin.display(description="Pregunta")
    def enunciado_resumido(self, obj):
        return obj.enunciado[:70]


@admin.register(OpcionRespuesta)
class OpcionRespuestaAdmin(admin.ModelAdmin):
    list_display = (
        "texto",
        "pregunta",
        "es_correcta",
        "orden",
    )
    list_filter = ("es_correcta",)
    search_fields = ("texto", "pregunta__enunciado")


@admin.register(IntentoEvaluacion)
class IntentoEvaluacionAdmin(admin.ModelAdmin):
    list_display = (
        "estudiante",
        "evaluacion",
        "fecha_inicio",
        "finalizado",
        "puntaje_obtenido",
        "porcentaje",
    )
    list_filter = ("finalizado", "evaluacion")
    search_fields = (
        "estudiante__username",
        "evaluacion__titulo",
    )
    readonly_fields = (
        "fecha_inicio",
        "fecha_finalizacion",
    )


@admin.register(RespuestaEstudiante)
class RespuestaEstudianteAdmin(admin.ModelAdmin):
    list_display = (
        "intento",
        "pregunta",
        "opcion_seleccionada",
        "es_correcta",
        "fecha_respuesta",
    )
    list_filter = ("es_correcta",)
    search_fields = (
        "pregunta__enunciado",
        "intento__estudiante__username",
    )
    readonly_fields = ("fecha_respuesta",)
