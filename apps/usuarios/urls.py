
from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("login/", views.iniciar_sesion, name="login"),
    path("perfil/", views.perfil, name="perfil"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),
]
