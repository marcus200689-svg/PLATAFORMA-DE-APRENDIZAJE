
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Recomendacion


@login_required
def lista_recomendaciones(request):
    recomendaciones = (
        Recomendacion.objects.filter(
            estudiante=request.user,
            intento__finalizado=True,
        )
        .select_related(
            "intento",
            "tema",
            "habilidad",
        )
        .order_by("-fecha_creacion")
    )

    return render(
        request,
        "recomendaciones/lista.html",
        {
            "recomendaciones": recomendaciones,
        },
    )
