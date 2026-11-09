
from django.urls import path
from apps.academico import views

urlpatterns = [

    # =========================================
    # RUTAS PARA ESTUDIANTES
    # =========================================

    path(
        "materias/",
        views.lista_materias,
        name="lista_materias"
    ),

    path(
        "materias/<int:materia_id>/",
        views.detalle_materia,
        name="detalle_materia"
    ),

    path(
        "habilidades/",
        views.lista_habilidades,
        name="lista_habilidades"
    ),

    # =========================================
    # CONSULTAS PARA DOCENTES
    # =========================================

    path(
        "profesor/materias/",
        views.profesor_lista_materias,
        name="profesor_materias"
    ),

    path(
        "profesor/temas/",
        views.profesor_lista_temas,
        name="profesor_temas"
    ),

    path(
        "profesor/habilidades/",
        views.profesor_lista_habilidades,
        name="profesor_habilidades"
    ),

    # =========================================
    # CREAR REGISTROS
    # =========================================

    path(
        "profesor/materias/crear/",
        views.profesor_crear_materia,
        name="profesor_crear_materia"
    ),

    path(
        "profesor/temas/crear/",
        views.profesor_crear_tema,
        name="profesor_crear_tema"
    ),

    path(
        "profesor/habilidades/crear/",
        views.profesor_crear_habilidad,
        name="profesor_crear_habilidad"
    ),

    # =========================================
    # EDITAR REGISTROS
    # =========================================

    path(
        "profesor/materias/editar/<int:materia_id>/",
        views.profesor_editar_materia,
        name="profesor_editar_materia"
    ),

    path(
        "profesor/temas/editar/<int:tema_id>/",
        views.profesor_editar_tema,
        name="profesor_editar_tema"
    ),

    path(
        "profesor/habilidades/editar/<int:habilidad_id>/",
        views.profesor_editar_habilidad,
        name="profesor_editar_habilidad"
    ),

    # =========================================
    # ACTIVAR / DESACTIVAR REGISTROS
    # =========================================

    path(
        "profesor/materias/estado/<int:materia_id>/",
        views.profesor_cambiar_estado_materia,
        name="profesor_estado_materia"
    ),

    path(
        "profesor/temas/estado/<int:tema_id>/",
        views.profesor_cambiar_estado_tema,
        name="profesor_estado_tema"
    ),

    path(
        "profesor/habilidades/estado/<int:habilidad_id>/",
        views.profesor_cambiar_estado_habilidad,
        name="profesor_estado_habilidad"
    ),
]
