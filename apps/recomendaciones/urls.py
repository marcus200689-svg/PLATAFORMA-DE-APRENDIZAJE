
from django.urls import path
from . import views
from . import profesor_views

app_name = "recomendaciones"

urlpatterns = [
    # Vista de recomendaciones para estudiantes
    path("", views.lista_recomendaciones, name="lista"),

    # Vista exclusiva para docentes
    path(
        "profesor/",
        profesor_views.profesor_lista_recomendaciones,
        name="profesor_lista"
    ),
]
