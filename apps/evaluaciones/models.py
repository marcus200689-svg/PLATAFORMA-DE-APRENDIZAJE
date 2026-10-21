
from django.conf import settings
from django.db import models


class Evaluacion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)

    materia = models.ForeignKey(
        "academico.Materia",
        on_delete=models.PROTECT,
        related_name="evaluaciones",
    )

    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.titulo} - {self.materia.nombre}"


class Pregunta(models.Model):
    evaluacion = models.ForeignKey(
        Evaluacion,
        on_delete=models.CASCADE,
        related_name="preguntas",
    )

    tema = models.ForeignKey(
        "academico.Tema",
        on_delete=models.PROTECT,
        related_name="preguntas",
        null=True,
        blank=True,
    )

    habilidades = models.ManyToManyField(
        "academico.Habilidad",
        related_name="preguntas",
        blank=True,
    )

    enunciado = models.TextField()
    puntaje = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=1.00,
    )
    orden = models.PositiveIntegerField(default=1)
    es_provisional = models.BooleanField(default=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"Pregunta {self.orden}: {self.enunciado[:60]}"


class OpcionRespuesta(models.Model):
    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name="opciones",
    )

    texto = models.CharField(max_length=500)
    es_correcta = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Opción de respuesta"
        verbose_name_plural = "Opciones de respuesta"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.pregunta} - {self.texto[:50]}"


class IntentoEvaluacion(models.Model):
    evaluacion = models.ForeignKey(
        Evaluacion,
        on_delete=models.PROTECT,
        related_name="intentos",
    )

    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="intentos_evaluacion",
    )

    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_finalizacion = models.DateTimeField(
        null=True,
        blank=True,
    )
    finalizado = models.BooleanField(default=False)

    puntaje_obtenido = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    class Meta:
        verbose_name = "Intento de evaluación"
        verbose_name_plural = "Intentos de evaluación"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"{self.estudiante} - {self.evaluacion}"


class RespuestaEstudiante(models.Model):
    intento = models.ForeignKey(
        IntentoEvaluacion,
        on_delete=models.CASCADE,
        related_name="respuestas",
    )

    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.PROTECT,
        related_name="respuestas_estudiantes",
    )

    opcion_seleccionada = models.ForeignKey(
        OpcionRespuesta,
        on_delete=models.PROTECT,
        related_name="respuestas_estudiantes",
        null=True,
        blank=True,
    )

    es_correcta = models.BooleanField(
        null=True,
        blank=True,
    )
    fecha_respuesta = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Respuesta del estudiante"
        verbose_name_plural = "Respuestas de los estudiantes"
        constraints = [
            models.UniqueConstraint(
                fields=["intento", "pregunta"],
                name="una_respuesta_por_pregunta_e_intento",
            ),
        ]

    def __str__(self):
        return f"{self.intento} - {self.pregunta}"
