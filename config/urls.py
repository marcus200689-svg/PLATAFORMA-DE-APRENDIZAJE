
from django.contrib import admin
from django.urls import path, include

from apps.usuarios import views as usuarios_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Página principal
    path("", usuarios_views.inicio, name="inicio"),

    # Aplicación de usuarios
    path("cuenta/", include("apps.usuarios.urls")),

    # Módulos de la plataforma
    path("evaluaciones/", include("apps.evaluaciones.urls")),
    path("academico/", include("apps.academico.urls")),
    path("resultados/", include("apps.resultados.urls")),
    path("recomendaciones/", include("apps.recomendaciones.urls")),
]
