
from django.contrib import admin
from .models import (
    ResultadoMateria,
    ResultadoTema,
    ResultadoHabilidad,
)


class ResultadoAdminBase(admin.ModelAdmin):
    list_display = (
        "intento",
        "estudiante",
        "puntaje_obtenido",
        "puntaje_maximo",
        "porcentaje",
        "fecha_calculo",
    )

    search_fields = (
        "intento__estudiante__username",
        "intento__estudiante__first_name",
        "intento__estudiante__last_name",
    )

    readonly_fields = ("fecha_calculo",)
    ordering = ("-fecha_calculo",)
    list_per_page = 20

    @admin.display(description="Estudiante", ordering="intento__estudiante__username")
    def estudiante(self, obj):
        return obj.intento.estudiante


@admin.register(ResultadoMateria)
class ResultadoMateriaAdmin(ResultadoAdminBase):
    list_display = ResultadoAdminBase.list_display + ("materia",)
    list_filter = ("materia", "fecha_calculo")
    search_fields = ResultadoAdminBase.search_fields + (
        "materia__nombre",
    )


@admin.register(ResultadoTema)
class ResultadoTemaAdmin(ResultadoAdminBase):
    list_display = ResultadoAdminBase.list_display + ("tema",)
    list_filter = ("tema__materia", "fecha_calculo")
    search_fields = ResultadoAdminBase.search_fields + (
        "tema__nombre",
        "tema__materia__nombre",
    )


@admin.register(ResultadoHabilidad)
class ResultadoHabilidadAdmin(ResultadoAdminBase):
    list_display = ResultadoAdminBase.list_display + ("habilidad",)
    list_filter = ("habilidad", "fecha_calculo")
    search_fields = ResultadoAdminBase.search_fields + (
        "habilidad__nombre",
    )
