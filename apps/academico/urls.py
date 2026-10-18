from django.urls import path

from apps.academico import views


urlpatterns = [
    path(
        "materias/",
        views.lista_materias,
        name="lista_materias",
    ),
    path(
        "materias/<int:materia_id>/",
        views.detalle_materia,
        name="detalle_materia",
    ),
    path(
        "habilidades/",
        views.lista_habilidades,
        name="lista_habilidades",
    ),
]