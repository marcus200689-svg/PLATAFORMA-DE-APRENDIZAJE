from django.contrib import admin

from apps.academico.models import Materia, Tema, Habilidad


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa", "fecha_creacion")
    list_filter = ("activa",)
    search_fields = ("nombre", "descripcion")


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "materia", "activo")
    list_filter = ("materia", "activo")
    search_fields = ("nombre", "materia__nombre")


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre", "descripcion")