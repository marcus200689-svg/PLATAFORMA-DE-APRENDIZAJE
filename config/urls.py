from django.contrib import admin
from django.urls import path, include

from apps.usuarios import views as usuarios_views


urlpatterns = [
    path("admin/", admin.site.urls),

    # Página principal
    path("", usuarios_views.inicio, name="inicio"),

    # Usuarios
    path("registro/", usuarios_views.registro, name="registro"),
    path("login/", usuarios_views.iniciar_sesion, name="login"),
    path("perfil/", usuarios_views.perfil, name="perfil"),
    path(
        "cerrar-sesion/",
        usuarios_views.cerrar_sesion,
        name="cerrar_sesion",
    ),
    path(
    "evaluaciones/",
    include("apps.evaluaciones.urls"),),

    # Módulo académico
    path("academico/", include("apps.academico.urls")),
]