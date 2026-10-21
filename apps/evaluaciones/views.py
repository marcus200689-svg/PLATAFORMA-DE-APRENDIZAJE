
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import (
    Evaluacion,
    IntentoEvaluacion,
    OpcionRespuesta,
    Pregunta,
    RespuestaEstudiante,
)
from .services import finalizar_evaluacion


@login_required
def lista_evaluaciones(request):
    evaluaciones = (
        Evaluacion.objects.filter(activa=True)
        .select_related("materia")
        .order_by("materia__nombre", "titulo")
    )

    return render(
        request,
        "evaluaciones/lista.html",
        {"evaluaciones": evaluaciones},
    )


@login_required
@require_POST
def iniciar_evaluacion(request, evaluacion_id):
    evaluacion = get_object_or_404(
        Evaluacion,
        pk=evaluacion_id,
        activa=True,
    )

    if not evaluacion.preguntas.filter(activa=True).exists():
        messages.error(
            request,
            "Esta evaluación todavía no tiene preguntas activas.",
        )
        return redirect("evaluaciones:lista")

    intento = IntentoEvaluacion.objects.create(
        evaluacion=evaluacion,
        estudiante=request.user,
    )

    return redirect(
        "evaluaciones:resolver",
        intento_id=intento.pk,
    )


@login_required
def resolver_evaluacion(request, intento_id):
    intento = get_object_or_404(
        IntentoEvaluacion.objects.select_related("evaluacion", "evaluacion__materia"),
        pk=intento_id,
        estudiante=request.user,
    )

    if intento.finalizado:
        return redirect(
            "evaluaciones:resultado",
            intento_id=intento.pk,
        )

    preguntas = (
        Pregunta.objects.filter(
            evaluacion=intento.evaluacion,
            activa=True,
        )
        .prefetch_related("opciones", "habilidades")
        .order_by("orden", "id")
    )

    return render(
        request,
        "evaluaciones/resolver.html",
        {
            "intento": intento,
            "evaluacion": intento.evaluacion,
            "preguntas": preguntas,
        },
    )


@login_required
@require_POST
@transaction.atomic
def enviar_respuestas(request, intento_id):
    intento = get_object_or_404(
        IntentoEvaluacion.objects.select_for_update(),
        pk=intento_id,
        estudiante=request.user,
    )

    if intento.finalizado:
        return redirect(
            "evaluaciones:resultado",
            intento_id=intento.pk,
        )

    preguntas = Pregunta.objects.filter(
        evaluacion=intento.evaluacion,
        activa=True,
    )

    for pregunta in preguntas:
        campo = f"pregunta_{pregunta.pk}"
        opcion_id = request.POST.get(campo)

        if not opcion_id:
            continue

        opcion = get_object_or_404(
            OpcionRespuesta,
            pk=opcion_id,
            pregunta=pregunta,
        )

        RespuestaEstudiante.objects.update_or_create(
            intento=intento,
            pregunta=pregunta,
            defaults={"opcion_seleccionada": opcion},
        )

    finalizar_evaluacion(intento)

    messages.success(
        request,
        "Tu evaluación se envió y calificó correctamente.",
    )

    return redirect(
        "evaluaciones:resultado",
        intento_id=intento.pk,
    )


@login_required
def resultado_evaluacion(request, intento_id):
    intento = get_object_or_404(
        IntentoEvaluacion.objects.select_related(
            "evaluacion",
            "evaluacion__materia",
        ),
        pk=intento_id,
        estudiante=request.user,
    )

    respuestas = (
        RespuestaEstudiante.objects.filter(intento=intento)
        .select_related("pregunta", "opcion_seleccionada")
        .order_by("pregunta__orden", "pregunta__id")
    )

    return render(
        request,
        "evaluaciones/resultado.html",
        {
            "intento": intento,
            "respuestas": respuestas,
        },
    )
