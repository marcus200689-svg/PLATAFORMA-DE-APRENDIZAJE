
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from .models import Evaluacion
from .forms import EvaluacionForm


def es_profesor_o_administrador(usuario):
    rol = getattr(usuario, "rol", "")

    return (
        rol == "docente"
        or rol == "administrador"
        or usuario.is_staff
        or usuario.is_superuser
    )


@login_required
def profesor_lista_evaluaciones(request):
    if not es_profesor_o_administrador(request.user):
        raise PermissionDenied(
            "No tienes permiso para administrar evaluaciones."
        )

    evaluaciones = Evaluacion.objects.select_related(
        "materia",
        "creada_por",
    ).order_by("-fecha_creacion")

    # Los profesores solo ven las evaluaciones que ellos crearon.
    # Los administradores autorizados pueden consultar todas.
    if not (
        request.user.is_staff
        or request.user.is_superuser
        or getattr(request.user, "rol", "") == "administrador"
    ):
        evaluaciones = evaluaciones.filter(
            creada_por=request.user
        )

    contexto = {
        "evaluaciones": evaluaciones,
    }

    return render(
        request,
        "profesores/evaluaciones_lista.html",
        contexto,
    )


@login_required
def profesor_crear_evaluacion(request):
    if not es_profesor_o_administrador(request.user):
        raise PermissionDenied(
            "No tienes permiso para crear evaluaciones."
        )

    if request.method == "POST":
        form = EvaluacionForm(request.POST)

        if form.is_valid():
            evaluacion = form.save(commit=False)

            # Se asigna el usuario autenticado como creador.
            # El formulario no permite elegir otro profesor.
            evaluacion.creada_por = request.user
            evaluacion.save()

            messages.success(
                request,
                "La evaluación se creó correctamente."
            )

            return redirect("evaluaciones:profesor_lista")
    else:
        form = EvaluacionForm()

    return render(
        request,
        "profesores/evaluacion_formulario.html",
        {
            "form": form,
            "titulo_pagina": "Crear evaluación",
        },
    )


@login_required
def profesor_editar_evaluacion(request, evaluacion_id):
    if not es_profesor_o_administrador(request.user):
        raise PermissionDenied(
            "No tienes permiso para editar evaluaciones."
        )

    evaluacion = get_object_or_404(
        Evaluacion,
        pk=evaluacion_id,
    )

    es_administrador = (
        request.user.is_staff
        or request.user.is_superuser
        or getattr(request.user, "rol", "") == "administrador"
    )

    # El profesor solo puede editar sus propias evaluaciones.
    if (
        not es_administrador
        and evaluacion.creada_por_id != request.user.pk
    ):
        raise PermissionDenied(
            "Solo puedes editar las evaluaciones que creaste."
        )

    if request.method == "POST":
        form = EvaluacionForm(
            request.POST,
            instance=evaluacion,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La evaluación se actualizó correctamente."
            )

            return redirect("evaluaciones:profesor_lista")
    else:
        form = EvaluacionForm(instance=evaluacion)

    return render(
        request,
        "profesores/evaluacion_formulario.html",
        {
            "form": form,
            "titulo_pagina": "Editar evaluación",
        },
    )
