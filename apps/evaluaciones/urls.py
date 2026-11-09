
from django.urls import path

from . import views
from . import profesor_views

app_name = "evaluaciones"

urlpatterns = [
    # Evaluaciones para estudiantes
    path(
        "",
        views.lista_evaluaciones,
        name="lista",
    ),

    path(
        "<int:evaluacion_id>/iniciar/",
        views.iniciar_evaluacion,
        name="iniciar",
    ),

    path(
        "intento/<int:intento_id>/",
        views.resolver_evaluacion,
        name="resolver",
    ),

    path(
        "intento/<int:intento_id>/enviar/",
        views.enviar_respuestas,
        name="enviar",
    ),

    path(
        "intento/<int:intento_id>/resultado/",
        views.resultado_evaluacion,
        name="resultado",
    ),

    # Administración de evaluaciones para docentes
    path(
        "profesor/",
        profesor_views.profesor_lista_evaluaciones,
        name="profesor_lista",
    ),

    path(
        "profesor/crear/",
        profesor_views.profesor_crear_evaluacion,
        name="profesor_crear",
    ),

    path(
        "profesor/<int:evaluacion_id>/editar/",
        profesor_views.profesor_editar_evaluacion,
        name="profesor_editar",
    ),

    # Administración de preguntas
    path(
        "profesor/<int:evaluacion_id>/preguntas/",
        profesor_views.profesor_lista_preguntas,
        name="profesor_preguntas",
    ),

    path(
        "profesor/<int:evaluacion_id>/preguntas/crear/",
        profesor_views.profesor_crear_pregunta,
        name="profesor_crear_pregunta",
    ),

    path(
        "profesor/<int:evaluacion_id>/preguntas/<int:pregunta_id>/editar/",
        profesor_views.profesor_editar_pregunta,
        name="profesor_editar_pregunta",
    ),
]
