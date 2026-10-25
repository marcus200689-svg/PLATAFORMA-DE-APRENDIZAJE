
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from apps.academico.models import Materia, Tema, Habilidad
from apps.evaluaciones.models import Evaluacion, Pregunta


def inicio(request):
    return render(request, "inicio.html")


def registro(request):
    return render(request, "usuarios/registro.html")


def iniciar_sesion(request):
    return render(request, "usuarios/login.html")


@login_required
def perfil(request):
    return render(request, "usuarios/perfil.html")


def cerrar_sesion(request):
    logout(request)
    return redirect("inicio")


@login_required
def panel_profesor(request):
    # Solo docentes y administradores pueden acceder.
    es_docente = getattr(request.user, "rol", "") == "docente"
    es_administrador = (
        request.user.is_staff or request.user.is_superuser
        or getattr(request.user, "rol", "") == "administrador"
    )

    if not (es_docente or es_administrador):
        raise PermissionDenied(
            "No tienes permiso para acceder al panel del profesor."
        )

    contexto = {
        "total_materias": Materia.objects.count(),
        "total_temas": Tema.objects.count(),
        "total_habilidades": Habilidad.objects.count(),
        "total_evaluaciones": Evaluacion.objects.count(),
        "total_preguntas": Pregunta.objects.count(),
        "evaluaciones": Evaluacion.objects.select_related(
            "materia"
        ).order_by("-fecha_creacion")[:5],
    }

    return render(request, "profesores/panel.html", contexto)
