
from django.contrib import admin
from .models import Materia, Tema, Habilidad


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    search_fields = ("nombre",)
    list_filter = ("activa",)
    ordering = ("nombre",)


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "materia")
    search_fields = ("nombre", "materia__nombre")
    list_filter = ("materia",)
    ordering = ("materia__nombre", "nombre")


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    search_fields = ("nombre",)
    list_filter = ("activa",)
    ordering = ("nombre",)
