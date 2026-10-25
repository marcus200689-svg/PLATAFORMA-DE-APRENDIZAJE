
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from apps.evaluaciones.models import IntentoEvaluacion
from .models import (
    ResultadoMateria,
    ResultadoTema,
    ResultadoHabilidad,
)


@login_required
def lista_resultados(request):
    """Muestra al usuario los intentos de evaluación que le pertenecen."""

    intentos = (
        IntentoEvaluacion.objects.filter(
            estudiante=request.user,
            finalizado=True,
        )
        .select_related("evaluacion", "evaluacion__materia")
        .order_by("-fecha_finalizacion")
    )

    return render(
        request,
        "resultados/lista.html",
        {"intentos": intentos},
    )


@login_required
def detalle_resultado(request, intento_id):
    """Muestra los resultados de materia, tema y habilidad de un intento."""

    intento = get_object_or_404(
        IntentoEvaluacion.objects.select_related(
            "evaluacion",
            "evaluacion__materia",
        ),
        pk=intento_id,
        estudiante=request.user,
        finalizado=True,
    )

    resultado_materia = ResultadoMateria.objects.filter(
        intento=intento,
    ).select_related("materia").first()

    resultados_temas = (
        ResultadoTema.objects.filter(intento=intento)
        .select_related("tema", "tema__materia")
        .order_by("tema__nombre")
    )

    resultados_habilidades = (
        ResultadoHabilidad.objects.filter(intento=intento)
        .select_related("habilidad")
        .order_by("habilidad__nombre")
    )

    return render(
        request,
        "resultados/detalle.html",
        {
            "intento": intento,
            "resultado_materia": resultado_materia,
            "resultados_temas": resultados_temas,
            "resultados_habilidades": resultados_habilidades,
        },
    )
