
from django.contrib import admin
from .models import Recomendacion


@admin.register(Recomendacion)
class RecomendacionAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "estudiante",
        "tipo",
        "prioridad",
        "porcentaje_referencia",
        "fecha_creacion",
    )
    list_filter = ("tipo", "prioridad")
    search_fields = (
        "titulo",
        "estudiante__username",
        "descripcion",
    )
    readonly_fields = ("fecha_creacion",)
    ordering = ("-fecha_creacion",)
