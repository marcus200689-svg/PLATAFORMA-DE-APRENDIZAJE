
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from apps.usuarios.models import Usuario
from .models import Recomendacion


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
        {"recomendaciones": recomendaciones},
    )
