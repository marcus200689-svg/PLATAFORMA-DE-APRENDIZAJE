
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

from apps.usuarios.models import Usuario
from apps.evaluaciones.models import IntentoEvaluacion
from .models import (
    ResultadoMateria,
    ResultadoTema,
    ResultadoHabilidad,
)


def requiere_estudiante(vista):
    @wraps(vista)
    def vista_protegida(request, *args, **kwargs):
        usuario = request.user

        if (
            usuario.rol != Usuario.Rol.ESTUDIANTE
            or usuario.is_staff
            or usuario.is_superuser
        ):
            raise PermissionDenied(
                "Esta sección está disponible únicamente para estudiantes."
            )

        return vista(request, *args, **kwargs)

    return vista_protegida


@login_required
@requiere_estudiante
def lista_resultados(request):
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
@requiere_estudiante
def detalle_resultado(request, intento_id):
    intento = get_object_or_404(
        IntentoEvaluacion.objects.select_related(
            "evaluacion",
            "evaluacion__materia",
        ),
        pk=intento_id,
        estudiante=request.user,
        finalizado=True,
    )

    resultado_materia = (
        ResultadoMateria.objects.filter(intento=intento)
        .select_related("materia")
        .first()
    )

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
