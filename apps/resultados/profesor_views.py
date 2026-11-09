
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.usuarios.decorators import requiere_docente

from .models import (
    ResultadoMateria,
    ResultadoTema,
    ResultadoHabilidad,
)


@login_required
@requiere_docente
def profesor_resultados_materia(request):

    resultados = (
        ResultadoMateria.objects.filter(
            intento__evaluacion__creada_por=request.user,
            intento__finalizado=True,
        )
        .select_related(
            "intento",
            "intento__estudiante",
            "intento__evaluacion",
            "materia",
        )
        .order_by("-fecha_calculo")
    )

    return render(
        request,
        "profesores/resultados_lista.html",
        {
            "resultados": resultados,
            "titulo_pagina": "Resultados por materia",
            "tipo_resultado": "materia",
            "seccion_activa": "resultado_materia",
        }
    )


@login_required
@requiere_docente
def profesor_resultados_tema(request):

    resultados = (
        ResultadoTema.objects.filter(
            intento__evaluacion__creada_por=request.user,
            intento__finalizado=True,
        )
        .select_related(
            "intento",
            "intento__estudiante",
            "intento__evaluacion",
            "tema",
            "tema__materia",
        )
        .order_by("-fecha_calculo")
    )

    return render(
        request,
        "profesores/resultados_lista.html",
        {
            "resultados": resultados,
            "titulo_pagina": "Resultados por tema",
            "tipo_resultado": "tema",
            "seccion_activa": "resultado_tema",
        }
    )


@login_required
@requiere_docente
def profesor_resultados_habilidad(request):

    resultados = (
        ResultadoHabilidad.objects.filter(
            intento__evaluacion__creada_por=request.user,
            intento__finalizado=True,
        )
        .select_related(
            "intento",
            "intento__estudiante",
            "intento__evaluacion",
            "habilidad",
        )
        .order_by("-fecha_calculo")
    )

    return render(
        request,
        "profesores/resultados_lista.html",
        {
            "resultados": resultados,
            "titulo_pagina": "Resultados por habilidad",
            "tipo_resultado": "habilidad",
            "seccion_activa": "resultado_habilidad",
        }
    )
