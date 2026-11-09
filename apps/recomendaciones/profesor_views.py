
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.usuarios.decorators import requiere_docente
from .models import Recomendacion


@login_required
@requiere_docente
def profesor_lista_recomendaciones(request):

    recomendaciones = (
        Recomendacion.objects.filter(
            intento__evaluacion__creada_por=request.user,
            intento__finalizado=True,
        )
        .select_related(
            "estudiante",
            "intento",
            "intento__evaluacion",
            "tema",
            "habilidad",
        )
        .order_by("-fecha_creacion")
    )

    return render(
        request,
        "profesores/recomendaciones.html",
        {
            "recomendaciones": recomendaciones,
            "titulo_pagina": "Recomendaciones",
            "seccion_activa": "recomendaciones",
        }
    )
