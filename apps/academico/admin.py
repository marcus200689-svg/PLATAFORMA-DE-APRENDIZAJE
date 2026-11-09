
from django.contrib import admin
from .models import Materia, Tema, Habilidad


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "activa",
        "fecha_creacion",
        "total_temas",
    )
    list_filter = ("activa", "fecha_creacion")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)
    readonly_fields = ("fecha_creacion",)
    list_per_page = 15

    @admin.display(description="Temas registrados")
    def total_temas(self, obj):
        return obj.temas.count()


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "materia",
        "activo",
    )
    list_filter = ("activo", "materia")
    search_fields = (
        "nombre",
        "descripcion",
        "materia__nombre",
    )
    ordering = ("materia__nombre", "nombre")
    list_per_page = 15
    autocomplete_fields = ("materia",)


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "activa",
    )
    list_filter = ("activa",)
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)
    list_per_page = 15
