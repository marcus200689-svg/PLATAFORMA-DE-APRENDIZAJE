
from django.urls import path

from . import views


app_name = "evaluaciones"

urlpatterns = [
    path("", views.lista_evaluaciones, name="lista"),

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
]
