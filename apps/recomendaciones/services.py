
from django.db import transaction

from apps.resultados.models import (
    ResultadoTema,
    ResultadoHabilidad,
)
from .models import Recomendacion


UMBRAL_REFUERZO = 60


@transaction.atomic
def generar_recomendaciones(intento_id):
    """
    Genera recomendaciones a partir de los resultados guardados.
    Si se vuelve a ejecutar para el mismo intento, reemplaza
    sus recomendaciones anteriores para evitar duplicados.
    """
    from apps.evaluaciones.models import IntentoEvaluacion

    intento = IntentoEvaluacion.objects.select_related(
        "estudiante",
        "evaluacion",
    ).get(
        pk=intento_id,
        finalizado=True,
    )

    # Solo se regeneran las recomendaciones de este intento.
    Recomendacion.objects.filter(intento=intento).delete()

    nuevas_recomendaciones = []

    resultados_temas = ResultadoTema.objects.filter(
        intento=intento,
    ).select_related("tema")

    for resultado in resultados_temas:
        if resultado.porcentaje < UMBRAL_REFUERZO:
            nuevas_recomendaciones.append(
                Recomendacion(
                    estudiante=intento.estudiante,
                    intento=intento,
                    tipo=Recomendacion.Tipo.TEMA,
                    titulo=f"Reforzar el tema: {resultado.tema.nombre}",
                    descripcion=(
                        f"Tu resultado en {resultado.tema.nombre} fue de "
                        f"{resultado.porcentaje} %. Te recomendamos repasar "
                        "los conceptos principales y resolver ejercicios "
                        "adicionales antes de volver a evaluarte."
                    ),
                    prioridad=(
                        Recomendacion.Prioridad.ALTA
                        if resultado.porcentaje < 40
                        else Recomendacion.Prioridad.MEDIA
                    ),
                    tema=resultado.tema,
                    porcentaje_referencia=resultado.porcentaje,
                )
            )

    resultados_habilidades = ResultadoHabilidad.objects.filter(
        intento=intento,
    ).select_related("habilidad")

    for resultado in resultados_habilidades:
        if resultado.porcentaje < UMBRAL_REFUERZO:
            nuevas_recomendaciones.append(
                Recomendacion(
                    estudiante=intento.estudiante,
                    intento=intento,
                    tipo=Recomendacion.Tipo.HABILIDAD,
                    titulo=(
                        f"Practicar la habilidad: "
                        f"{resultado.habilidad.nombre}"
                    ),
                    descripcion=(
                        f"Tu resultado en {resultado.habilidad.nombre} fue "
                        f"de {resultado.porcentaje} %. Puedes practicar con "
                        "actividades graduales y revisar los procedimientos "
                        "de las preguntas que contestaste incorrectamente."
                    ),
                    prioridad=(
                        Recomendacion.Prioridad.ALTA
                        if resultado.porcentaje < 40
                        else Recomendacion.Prioridad.MEDIA
                    ),
                    habilidad=resultado.habilidad,
                    porcentaje_referencia=resultado.porcentaje,
                )
            )

    # Si todas las áreas evaluadas alcanzan el umbral, se registra
    # una recomendación general positiva.
    if not nuevas_recomendaciones:
        nuevas_recomendaciones.append(
            Recomendacion(
                estudiante=intento.estudiante,
                intento=intento,
                tipo=Recomendacion.Tipo.GENERAL,
                titulo="Continúa con tu aprendizaje",
                descripcion=(
                    "En las áreas analizadas no se detectaron resultados "
                    "inferiores al umbral de refuerzo del proyecto. "
                    "Continúa practicando para consolidar tus conocimientos."
                ),
                prioridad=Recomendacion.Prioridad.BAJA,
            )
        )

    Recomendacion.objects.bulk_create(nuevas_recomendaciones)

    return nuevas_recomendaciones
