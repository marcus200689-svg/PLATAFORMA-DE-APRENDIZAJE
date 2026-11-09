
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from .models import Pregunta
from .forms import PreguntaForm, OpcionRespuestaFormSet

from .models import Evaluacion
from .forms import EvaluacionForm
from django.views.decorators.cache import never_cache


def es_profesor_o_administrador(usuario):
    rol = getattr(usuario, "rol", "")

    return (
        rol == "docente"
        or rol == "administrador"
        or usuario.is_staff
        or usuario.is_superuser
    )

@never_cache
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

@never_cache
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

@never_cache
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

@never_cache
@login_required
def profesor_lista_preguntas(request, evaluacion_id):
    if not es_profesor_o_administrador(request.user):
        raise PermissionDenied(
            "No tienes permiso para administrar preguntas."
        )

    es_administrador = (
        request.user.is_staff
        or request.user.is_superuser
        or getattr(request.user, "rol", "") == "administrador"
    )

    evaluacion = get_object_or_404(
        Evaluacion,
        pk=evaluacion_id,
    )

    if (
        not es_administrador
        and evaluacion.creada_por_id != request.user.pk
    ):
        raise PermissionDenied(
            "No puedes administrar preguntas de esta evaluación."
        )

    preguntas = evaluacion.preguntas.prefetch_related(
        "habilidades",
        "opciones",
    ).select_related("tema").order_by("orden", "id")

    return render(
        request,
        "profesores/preguntas_lista.html",
        {
            "evaluacion": evaluacion,
            "preguntas": preguntas,
        },
    )

@never_cache
@login_required
def profesor_crear_pregunta(request, evaluacion_id):
    if not es_profesor_o_administrador(request.user):
        raise PermissionDenied(
            "No tienes permiso para crear preguntas."
        )

    es_administrador = (
        request.user.is_staff
        or request.user.is_superuser
        or getattr(request.user, "rol", "") == "administrador"
    )

    evaluacion = get_object_or_404(
        Evaluacion,
        pk=evaluacion_id,
    )

    if (
        not es_administrador
        and evaluacion.creada_por_id != request.user.pk
    ):
        raise PermissionDenied(
            "No puedes agregar preguntas a esta evaluación."
        )

    if request.method == "POST":
        form = PreguntaForm(request.POST)

        pregunta_temporal = Pregunta(evaluacion=evaluacion)

        formset = OpcionRespuestaFormSet(
            request.POST,
            instance=pregunta_temporal,
            prefix="opciones",
        )

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                pregunta = form.save(commit=False)
                pregunta.evaluacion = evaluacion
                pregunta.save()
                form.save_m2m()

                formset.instance = pregunta
                formset.save()

            messages.success(
                request,
                "La pregunta y sus opciones se guardaron correctamente."
            )

            return redirect(
                "evaluaciones:profesor_preguntas",
                evaluacion_id=evaluacion.id,
            )

    else:
        form = PreguntaForm()

        pregunta_temporal = Pregunta(evaluacion=evaluacion)

        formset = OpcionRespuestaFormSet(
            instance=pregunta_temporal,
            prefix="opciones",
        )

    return render(
        request,
        "profesores/pregunta_formulario.html",
        {
            "form": form,
            "formset": formset,
            "evaluacion": evaluacion,
            "titulo_pagina": "Agregar pregunta",
        },
    )

@never_cache
@login_required
def profesor_editar_pregunta(request, evaluacion_id, pregunta_id):
    if not es_profesor_o_administrador(request.user):
        raise PermissionDenied(
            "No tienes permiso para editar preguntas."
        )

    es_administrador = (
        request.user.is_staff
        or request.user.is_superuser
        or getattr(request.user, "rol", "") == "administrador"
    )

    evaluacion = get_object_or_404(
        Evaluacion,
        pk=evaluacion_id,
    )

    if (
        not es_administrador
        and evaluacion.creada_por_id != request.user.pk
    ):
        raise PermissionDenied(
            "No puedes modificar esta evaluación."
        )

    pregunta = get_object_or_404(
        Pregunta,
        pk=pregunta_id,
        evaluacion=evaluacion,
    )

    if request.method == "POST":
        form = PreguntaForm(
            request.POST,
            instance=pregunta,
        )

        formset = OpcionRespuestaFormSet(
            request.POST,
            instance=pregunta,
            prefix="opciones",
        )

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()

            messages.success(
                request,
                "La pregunta se actualizó correctamente."
            )

            return redirect(
                "evaluaciones:profesor_preguntas",
                evaluacion_id=evaluacion.id,
            )

    else:
        form = PreguntaForm(instance=pregunta)

        formset = OpcionRespuestaFormSet(
            instance=pregunta,
            prefix="opciones",
        )

    return render(
        request,
        "profesores/pregunta_formulario.html",
        {
            "form": form,
            "formset": formset,
            "evaluacion": evaluacion,
            "titulo_pagina": "Editar pregunta",
        },
    )
