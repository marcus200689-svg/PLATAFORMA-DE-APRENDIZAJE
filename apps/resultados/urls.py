
from django.urls import path

from . import views

app_name = "resultados"

urlpatterns = [
    path("", views.lista_resultados, name="lista"),
    path(
        "<int:intento_id>/",
        views.detalle_resultado,
        name="detalle",
    ),
]
