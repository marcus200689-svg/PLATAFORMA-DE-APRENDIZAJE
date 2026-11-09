
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
    fields = ("texto", "es_correcta", "orden")


class PreguntaInline(admin.StackedInline):
    model = Pregunta
    extra = 1
    filter_horizontal = ("habilidades",)
    show_change_link = True


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "materia",
        "activa",
        "fecha_creacion",
    )
    list_filter = ("activa", "materia")
    search_fields = ("titulo", "materia__nombre")
    ordering = ("materia__nombre", "titulo")
    readonly_fields = ("fecha_creacion",)
    list_per_page = 15
    inlines = [PreguntaInline]


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = (
        "enunciado",
        "evaluacion",
        "tema",
        "puntaje",
        "es_provisional",
        "activa",
    )
    list_filter = (
        "activa",
        "es_provisional",
        "evaluacion",
        "tema",
    )
    search_fields = (
        "enunciado",
        "evaluacion__titulo",
        "tema__nombre",
    )
    filter_horizontal = ("habilidades",)
    list_editable = ("activa",)
    list_per_page = 15
    inlines = [OpcionRespuestaInline]


@admin.register(OpcionRespuesta)
class OpcionRespuestaAdmin(admin.ModelAdmin):
    list_display = (
        "texto",
        "pregunta",
        "es_correcta",
        "orden",
    )
    list_filter = ("es_correcta",)
    search_fields = (
        "texto",
        "pregunta__enunciado",
    )
    ordering = ("pregunta", "orden")
    list_per_page = 20


@admin.register(IntentoEvaluacion)
class IntentoEvaluacionAdmin(admin.ModelAdmin):
    list_display = (
        "estudiante",
        "evaluacion",
        "fecha_inicio",
        "finalizado",
        "porcentaje",
    )
    list_filter = ("finalizado", "evaluacion")
    search_fields = (
        "estudiante__username",
        "estudiante__first_name",
        "estudiante__last_name",
        "evaluacion__titulo",
    )
    readonly_fields = (
        "fecha_inicio",
        "fecha_finalizacion",
        "puntaje_obtenido",
        "porcentaje",
    )
    ordering = ("-fecha_inicio",)
    list_per_page = 20


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
        "intento__evaluacion__titulo",
    )
    readonly_fields = ("fecha_respuesta",)
    list_per_page = 20
