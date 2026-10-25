
from django.contrib import admin
from .models import (
    ResultadoMateria,
    ResultadoTema,
    ResultadoHabilidad,
)


@admin.register(ResultadoMateria)
class ResultadoMateriaAdmin(admin.ModelAdmin):
    list_display = (
        "intento",
        "materia",
        "puntaje_obtenido",
        "puntaje_maximo",
        "porcentaje",
        "fecha_calculo",
    )
    list_filter = ("materia",)
    search_fields = ("materia__nombre", "intento__estudiante__username")
    readonly_fields = ("fecha_calculo",)


@admin.register(ResultadoTema)
class ResultadoTemaAdmin(admin.ModelAdmin):
    list_display = (
        "intento",
        "tema",
        "puntaje_obtenido",
        "puntaje_maximo",
        "porcentaje",
        "fecha_calculo",
    )
    list_filter = ("tema__materia",)
    search_fields = ("tema__nombre", "intento__estudiante__username")
    readonly_fields = ("fecha_calculo",)


@admin.register(ResultadoHabilidad)
class ResultadoHabilidadAdmin(admin.ModelAdmin):
    list_display = (
        "intento",
        "habilidad",
        "puntaje_obtenido",
        "puntaje_maximo",
        "porcentaje",
        "fecha_calculo",
    )
    list_filter = ("habilidad",)
    search_fields = (
        "habilidad__nombre",
        "intento__estudiante__username",
    )
    readonly_fields = ("fecha_calculo",)
