
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import IntentoEvaluacion, RespuestaEstudiante


def validar_evaluacion(evaluacion):
    """
    Comprueba que la evaluación tenga preguntas y opciones válidas
    antes de permitir que un estudiante la responda.
    """
    preguntas = evaluacion.preguntas.filter(activa=True).prefetch_related(
        "opciones"
    )

    if not preguntas.exists():
        raise ValidationError(
            "La evaluación debe tener al menos una pregunta activa."
        )

    for pregunta in preguntas:
        opciones = list(pregunta.opciones.all())

        if len(opciones) < 2:
            raise ValidationError(
                f"La pregunta {pregunta.orden} debe tener al menos "
                "dos opciones de respuesta."
            )

        correctas = sum(1 for opcion in opciones if opcion.es_correcta)

        if correctas != 1:
            raise ValidationError(
                f"La pregunta {pregunta.orden} debe tener exactamente "
                "una opción correcta."
            )

        if pregunta.puntaje <= 0:
            raise ValidationError(
                f"La pregunta {pregunta.orden} debe tener un puntaje mayor que cero."
            )

    return True


def calcular_puntaje_maximo(intento):
    preguntas = intento.evaluacion.preguntas.filter(activa=True)

    return sum(
        (pregunta.puntaje for pregunta in preguntas),
        Decimal("0.00"),
    )


def calcular_calificacion(intento):
    preguntas = intento.evaluacion.preguntas.filter(activa=True)

    puntaje_maximo = Decimal("0.00")
    puntaje_obtenido = Decimal("0.00")

    for pregunta in preguntas:
        if pregunta.puntaje <= 0:
            raise ValidationError(
                f"La pregunta {pregunta.orden} tiene un puntaje inválido."
            )

        puntaje_maximo += pregunta.puntaje

        respuesta = (
            RespuestaEstudiante.objects.filter(
                intento=intento,
                pregunta=pregunta,
            )
            .select_related("opcion_seleccionada")
            .first()
        )

        if respuesta is None or respuesta.opcion_seleccionada is None:
            continue

        opcion = respuesta.opcion_seleccionada

        correcta = (
            opcion.pregunta_id == pregunta.id
            and opcion.es_correcta
        )

        respuesta.es_correcta = correcta
        respuesta.save(update_fields=["es_correcta"])

        if correcta:
            puntaje_obtenido += pregunta.puntaje

    if puntaje_maximo <= 0:
        raise ValidationError(
            "No se puede calificar una evaluación sin preguntas puntuables."
        )

    porcentaje = (
        puntaje_obtenido / puntaje_maximo * Decimal("100")
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return {
        "puntaje_obtenido": puntaje_obtenido,
        "puntaje_maximo": puntaje_maximo,
        "porcentaje": porcentaje,
    }


@transaction.atomic
def finalizar_evaluacion(intento):
    intento = IntentoEvaluacion.objects.select_for_update().get(
        pk=intento.pk
    )

    if intento.finalizado:
        return {
            "puntaje_obtenido": intento.puntaje_obtenido,
            "puntaje_maximo": calcular_puntaje_maximo(intento),
            "porcentaje": intento.porcentaje,
        }

    validar_evaluacion(intento.evaluacion)

    resultado = calcular_calificacion(intento)

    intento.puntaje_obtenido = resultado["puntaje_obtenido"]
    intento.porcentaje = resultado["porcentaje"]
    intento.fecha_finalizacion = timezone.now()
    intento.finalizado = True

    intento.save(
        update_fields=[
            "puntaje_obtenido",
            "porcentaje",
            "fecha_finalizacion",
            "finalizado",
        ]
    )

    return resultado
