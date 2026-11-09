
from django.urls import path
from . import profesor_views

from . import views

app_name = "resultados"

urlpatterns = [
    path("", views.lista_resultados, name="lista"),
    path(
        "<int:intento_id>/",
        views.detalle_resultado,
        name="detalle",
    ),
    path(
        "profesor/materias/",
        profesor_views.profesor_resultados_materia,
        name="profesor_materias"),
    path(
        "profesor/temas/",
        profesor_views.profesor_resultados_tema,
        name="profesor_temas"),
    path(
        "profesor/habilidades/",
        profesor_views.profesor_resultados_habilidad,
        name="profesor_habilidades"),

]

