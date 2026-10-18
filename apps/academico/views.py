from django.shortcuts import render, get_object_or_404

from apps.academico.models import Materia, Tema, Habilidad


def lista_materias(request):
    materias = Materia.objects.filter(activa=True)

    return render(
        request,
        "academico/materias.html",
        {"materias": materias},
    )


def detalle_materia(request, materia_id):
    materia = get_object_or_404(
        Materia,
        id=materia_id,
        activa=True,
    )

    temas = Tema.objects.filter(
        materia=materia,
        activo=True,
    )

    return render(
        request,
        "academico/detalle_materia.html",
        {
            "materia": materia,
            "temas": temas,
        },
    )


def lista_habilidades(request):
    habilidades = Habilidad.objects.filter(activa=True)

    return render(
        request,
        "academico/habilidades.html",
        {"habilidades": habilidades},
    )