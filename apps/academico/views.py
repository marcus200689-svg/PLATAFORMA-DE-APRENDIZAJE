
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.academico.models import Materia, Tema, Habilidad
from apps.academico.forms import MateriaForm, TemaForm, HabilidadForm
from apps.usuarios.decorators import requiere_docente


# =====================================================
# VISTAS PARA ESTUDIANTES
# =====================================================

def lista_materias(request):
    materias = Materia.objects.filter(
        activa=True
    ).order_by("nombre")

    return render(
        request,
        "academico/materias.html",
        {"materias": materias},
    )


def detalle_materia(request, materia_id):
    materia = get_object_or_404(
        Materia,
        id=materia_id,
        activa=True,
    )

    temas = Tema.objects.filter(
        materia=materia,
        activo=True,
    ).order_by("nombre")

    return render(
        request,
        "academico/detalle_materia.html",
        {
            "materia": materia,
            "temas": temas,
        },
    )


def lista_habilidades(request):
    habilidades = Habilidad.objects.filter(
        activa=True
    ).order_by("nombre")

    return render(
        request,
        "academico/habilidades.html",
        {"habilidades": habilidades},
    )


# =====================================================
# VISTAS DE CONSULTA PARA DOCENTES
# =====================================================

@login_required
@requiere_docente
def profesor_lista_materias(request):
    # Muestra materias activas e inactivas.
    materias = Materia.objects.all().order_by("nombre")

    return render(
        request,
        "profesores/academico_lista.html",
        {
            "titulo_pagina": "Materias",
            "descripcion_pagina": "Administra las materias de la plataforma.",
            "elementos": materias,
            "tipo_lista": "materias",
            "seccion_activa": "materias",
        },
    )


@login_required
@requiere_docente
def profesor_lista_temas(request):
    # Muestra temas activos e inactivos.
    temas = Tema.objects.select_related(
        "materia"
    ).order_by(
        "materia__nombre",
        "nombre",
    )

    return render(
        request,
        "profesores/academico_lista.html",
        {
            "titulo_pagina": "Temas",
            "descripcion_pagina": "Administra los temas organizados por materia.",
            "elementos": temas,
            "tipo_lista": "temas",
            "seccion_activa": "temas",
        },
    )


@login_required
@requiere_docente
def profesor_lista_habilidades(request):
    # Muestra habilidades activas e inactivas.
    habilidades = Habilidad.objects.all().order_by("nombre")

    return render(
        request,
        "profesores/academico_lista.html",
        {
            "titulo_pagina": "Habilidades",
            "descripcion_pagina": "Administra las habilidades que se evalúan en la plataforma.",
            "elementos": habilidades,
            "tipo_lista": "habilidades",
            "seccion_activa": "habilidades",
        },
    )


# =====================================================
# CREAR MATERIAS
# =====================================================

@login_required
@requiere_docente
def profesor_crear_materia(request):

    if request.method == "POST":
        formulario = MateriaForm(request.POST)

        if formulario.is_valid():
            materia = formulario.save()

            messages.success(
                request,
                f"La materia '{materia.nombre}' se creó correctamente.",
            )

            return redirect("profesor_materias")

    else:
        formulario = MateriaForm()

    return render(
        request,
        "profesores/academico_formulario.html",
        {
            "formulario": formulario,
            "titulo_pagina": "Crear materia",
            "descripcion_pagina": "Registra una nueva materia.",
            "seccion_activa": "materias",
            "url_regreso": "profesor_materias",
        },
    )


# =====================================================
# EDITAR MATERIAS
# =====================================================

@login_required
@requiere_docente
def profesor_editar_materia(request, materia_id):

    materia = get_object_or_404(
        Materia,
        id=materia_id,
    )

    if request.method == "POST":
        formulario = MateriaForm(
            request.POST,
            instance=materia,
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                "La materia se actualizó correctamente.",
            )

            return redirect("profesor_materias")

    else:
        formulario = MateriaForm(instance=materia)

    return render(
        request,
        "profesores/academico_formulario.html",
        {
            "formulario": formulario,
            "titulo_pagina": "Editar materia",
            "descripcion_pagina": "Modifica la información de esta materia.",
            "seccion_activa": "materias",
            "url_regreso": "profesor_materias",
        },
    )


# =====================================================
# ACTIVAR / DESACTIVAR MATERIAS
# =====================================================

@login_required
@requiere_docente
@require_POST
def profesor_cambiar_estado_materia(request, materia_id):

    materia = get_object_or_404(
        Materia,
        id=materia_id,
    )

    materia.activa = not materia.activa

    materia.save(
        update_fields=["activa"]
    )

    messages.success(
        request,
        f"La materia '{materia.nombre}' cambió de estado.",
    )

    return redirect("profesor_materias")


# =====================================================
# CREAR TEMAS
# =====================================================

@login_required
@requiere_docente
def profesor_crear_tema(request):

    if request.method == "POST":
        formulario = TemaForm(request.POST)

        if formulario.is_valid():
            tema = formulario.save()

            messages.success(
                request,
                f"El tema '{tema.nombre}' se creó correctamente.",
            )

            return redirect("profesor_temas")

    else:
        formulario = TemaForm()

    return render(
        request,
        "profesores/academico_formulario.html",
        {
            "formulario": formulario,
            "titulo_pagina": "Crear tema",
            "descripcion_pagina": "Registra un tema y relaciónalo con una materia.",
            "seccion_activa": "temas",
            "url_regreso": "profesor_temas",
        },
    )


# =====================================================
# EDITAR TEMAS
# =====================================================

@login_required
@requiere_docente
def profesor_editar_tema(request, tema_id):

    tema = get_object_or_404(
        Tema,
        id=tema_id,
    )

    if request.method == "POST":
        formulario = TemaForm(
            request.POST,
            instance=tema,
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                "El tema se actualizó correctamente.",
            )

            return redirect("profesor_temas")

    else:
        formulario = TemaForm(instance=tema)

    return render(
        request,
        "profesores/academico_formulario.html",
        {
            "formulario": formulario,
            "titulo_pagina": "Editar tema",
            "descripcion_pagina": "Modifica la información del tema.",
            "seccion_activa": "temas",
            "url_regreso": "profesor_temas",
        },
    )


# =====================================================
# ACTIVAR / DESACTIVAR TEMAS
# =====================================================

@login_required
@requiere_docente
@require_POST
def profesor_cambiar_estado_tema(request, tema_id):

    tema = get_object_or_404(
        Tema,
        id=tema_id,
    )

    tema.activo = not tema.activo

    tema.save(
        update_fields=["activo"]
    )

    messages.success(
        request,
        f"El tema '{tema.nombre}' cambió de estado.",
    )

    return redirect("profesor_temas")


# =====================================================
# CREAR HABILIDADES
# =====================================================

@login_required
@requiere_docente
def profesor_crear_habilidad(request):

    if request.method == "POST":
        formulario = HabilidadForm(request.POST)

        if formulario.is_valid():
            habilidad = formulario.save()

            messages.success(
                request,
                f"La habilidad '{habilidad.nombre}' se creó correctamente.",
            )

            return redirect("profesor_habilidades")

    else:
        formulario = HabilidadForm()

    return render(
        request,
        "profesores/academico_formulario.html",
        {
            "formulario": formulario,
            "titulo_pagina": "Crear habilidad",
            "descripcion_pagina": "Registra una nueva habilidad de aprendizaje.",
            "seccion_activa": "habilidades",
            "url_regreso": "profesor_habilidades",
        },
    )


# =====================================================
# EDITAR HABILIDADES
# =====================================================

@login_required
@requiere_docente
def profesor_editar_habilidad(request, habilidad_id):

    habilidad = get_object_or_404(
        Habilidad,
        id=habilidad_id,
    )

    if request.method == "POST":
        formulario = HabilidadForm(
            request.POST,
            instance=habilidad,
        )

        if formulario.is_valid():
            formulario.save()

            messages.success(
                request,
                "La habilidad se actualizó correctamente.",
            )

            return redirect("profesor_habilidades")

    else:
        formulario = HabilidadForm(instance=habilidad)

    return render(
        request,
        "profesores/academico_formulario.html",
        {
            "formulario": formulario,
            "titulo_pagina": "Editar habilidad",
            "descripcion_pagina": "Modifica la información de la habilidad.",
            "seccion_activa": "habilidades",
            "url_regreso": "profesor_habilidades",
        },
    )


# =====================================================
# ACTIVAR / DESACTIVAR HABILIDADES
# =====================================================

@login_required
@requiere_docente
@require_POST
def profesor_cambiar_estado_habilidad(request, habilidad_id):

    habilidad = get_object_or_404(
        Habilidad,
        id=habilidad_id,
    )

    habilidad.activa = not habilidad.activa

    habilidad.save(
        update_fields=["activa"]
    )

    messages.success(
        request,
        f"La habilidad '{habilidad.nombre}' cambió de estado.",
    )

    return redirect("profesor_habilidades")
