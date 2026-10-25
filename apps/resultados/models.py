
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ResultadoMateria(models.Model):
    """Resumen del rendimiento del estudiante en una materia."""

    intento = models.ForeignKey(
        "evaluaciones.IntentoEvaluacion",
        on_delete=models.CASCADE,
        related_name="resultados_materia",
    )
    materia = models.ForeignKey(
        "academico.Materia",
        on_delete=models.PROTECT,
        related_name="resultados",
    )
    puntaje_obtenido = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    puntaje_maximo = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    fecha_calculo = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Resultado por materia"
        verbose_name_plural = "Resultados por materia"
        constraints = [
            models.UniqueConstraint(
                fields=["intento", "materia"],
                name="resultado_unico_materia_por_intento",
            ),
        ]

    def __str__(self):
        return f"{self.materia.nombre}: {self.porcentaje}%"


class ResultadoTema(models.Model):
    """Resumen del rendimiento del estudiante en un tema."""

    intento = models.ForeignKey(
        "evaluaciones.IntentoEvaluacion",
        on_delete=models.CASCADE,
        related_name="resultados_tema",
    )
    tema = models.ForeignKey(
        "academico.Tema",
        on_delete=models.PROTECT,
        related_name="resultados",
    )
    puntaje_obtenido = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    puntaje_maximo = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    fecha_calculo = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Resultado por tema"
        verbose_name_plural = "Resultados por tema"
        constraints = [
            models.UniqueConstraint(
                fields=["intento", "tema"],
                name="resultado_unico_tema_por_intento",
            ),
        ]

    def __str__(self):
        return f"{self.tema.nombre}: {self.porcentaje}%"


class ResultadoHabilidad(models.Model):
    """Resumen del rendimiento del estudiante en una habilidad."""

    intento = models.ForeignKey(
        "evaluaciones.IntentoEvaluacion",
        on_delete=models.CASCADE,
        related_name="resultados_habilidad",
    )
    habilidad = models.ForeignKey(
        "academico.Habilidad",
        on_delete=models.PROTECT,
        related_name="resultados",
    )
    puntaje_obtenido = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    puntaje_maximo = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    fecha_calculo = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Resultado por habilidad"
        verbose_name_plural = "Resultados por habilidad"
        constraints = [
            models.UniqueConstraint(
                fields=["intento", "habilidad"],
                name="resultado_unico_habilidad_por_intento",
            ),
        ]

    def __str__(self):
        return f"{self.habilidad.nombre}: {self.porcentaje}%"
