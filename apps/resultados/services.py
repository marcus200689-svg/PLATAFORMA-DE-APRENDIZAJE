
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.evaluaciones.models import (
    IntentoEvaluacion,
    RespuestaEstudiante,
)
from .models import (
    ResultadoMateria,
    ResultadoTema,
    ResultadoHabilidad,
)


def calcular_porcentaje(puntaje_obtenido, puntaje_maximo):
    """Calcula un porcentaje con dos decimales."""
    if puntaje_maximo <= 0:
        return Decimal("0.00")

    return (
        puntaje_obtenido / puntaje_maximo * Decimal("100")
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


@transaction.atomic
def generar_resultados(intento_id):
    """
    Genera o actualiza los resultados por materia, tema y habilidad
    para un intento de evaluación finalizado.
    """
    intento = (
        IntentoEvaluacion.objects.select_for_update()
        .select_related("evaluacion", "evaluacion__materia")
        .get(pk=intento_id)
    )

    if not intento.finalizado:
        raise ValidationError(
            "No se pueden generar resultados de una evaluación sin finalizar."
        )

    materia = intento.evaluacion.materia
    preguntas = list(
        intento.evaluacion.preguntas.filter(activa=True)
        .prefetch_related("habilidades")
        .select_related("tema")
    )

    if not preguntas:
        raise ValidationError(
            "La evaluación no tiene preguntas activas para analizar."
        )

    respuestas = {
        respuesta.pregunta_id: respuesta
        for respuesta in RespuestaEstudiante.objects.filter(
            intento=intento,
            pregunta_id__in=[pregunta.id for pregunta in preguntas],
        ).select_related("opcion_seleccionada")
    }

    # Acumuladores por materia, tema y habilidad.
    materia_obtenido = Decimal("0.00")
    materia_maximo = Decimal("0.00")

    temas = {}
    habilidades = {}

    for pregunta in preguntas:
        puntaje = pregunta.puntaje

        if puntaje <= 0:
            raise ValidationError(
                f"La pregunta {pregunta.orden} tiene un puntaje inválido."
            )

        respuesta = respuestas.get(pregunta.id)
        es_correcta = bool(
            respuesta
            and respuesta.opcion_seleccionada
            and respuesta.opcion_seleccionada.pregunta_id == pregunta.id
            and respuesta.opcion_seleccionada.es_correcta
        )

        obtenido = puntaje if es_correcta else Decimal("0.00")

        # Resultado de la materia.
        materia_obtenido += obtenido
        materia_maximo += puntaje

        # Resultado del tema asociado a la pregunta.
        if pregunta.tema_id:
            if pregunta.tema_id not in temas:
                temas[pregunta.tema_id] = {
                    "tema": pregunta.tema,
                    "obtenido": Decimal("0.00"),
                    "maximo": Decimal("0.00"),
                }

            temas[pregunta.tema_id]["obtenido"] += obtenido
            temas[pregunta.tema_id]["maximo"] += puntaje

        # Resultado de cada habilidad asociada a la pregunta.
        for habilidad in pregunta.habilidades.all():
            if habilidad.id not in habilidades:
                habilidades[habilidad.id] = {
                    "habilidad": habilidad,
                    "obtenido": Decimal("0.00"),
                    "maximo": Decimal("0.00"),
                }

            habilidades[habilidad.id]["obtenido"] += obtenido
            habilidades[habilidad.id]["maximo"] += puntaje

    # Guardar el resultado general de la materia.
    ResultadoMateria.objects.update_or_create(
        intento=intento,
        materia=materia,
        defaults={
            "puntaje_obtenido": materia_obtenido,
            "puntaje_maximo": materia_maximo,
            "porcentaje": calcular_porcentaje(
                materia_obtenido,
                materia_maximo,
            ),
        },
    )

    # Guardar o actualizar los resultados por tema.
    for datos in temas.values():
        ResultadoTema.objects.update_or_create(
            intento=intento,
            tema=datos["tema"],
            defaults={
                "puntaje_obtenido": datos["obtenido"],
                "puntaje_maximo": datos["maximo"],
                "porcentaje": calcular_porcentaje(
                    datos["obtenido"],
                    datos["maximo"],
                ),
            },
        )

    # Guardar o actualizar los resultados por habilidad.
    for datos in habilidades.values():
        ResultadoHabilidad.objects.update_or_create(
            intento=intento,
            habilidad=datos["habilidad"],
            defaults={
                "puntaje_obtenido": datos["obtenido"],
                "puntaje_maximo": datos["maximo"],
                "porcentaje": calcular_porcentaje(
                    datos["obtenido"],
                    datos["maximo"],
                ),
            },
        )

    return {
        "materia": {
            "nombre": materia.nombre,
            "puntaje_obtenido": materia_obtenido,
            "puntaje_maximo": materia_maximo,
            "porcentaje": calcular_porcentaje(
                materia_obtenido,
                materia_maximo,
            ),
        },
        "temas": temas,
        "habilidades": habilidades,
    }
