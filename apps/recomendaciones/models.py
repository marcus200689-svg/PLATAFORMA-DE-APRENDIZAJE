
from django.conf import settings
from django.db import models


class Recomendacion(models.Model):
    class Tipo(models.TextChoices):
        MATERIA = "materia", "Materia"
        TEMA = "tema", "Tema"
        HABILIDAD = "habilidad", "Habilidad"
        GENERAL = "general", "General"

    class Prioridad(models.TextChoices):
        BAJA = "baja", "Baja"
        MEDIA = "media", "Media"
        ALTA = "alta", "Alta"

    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recomendaciones",
    )

    intento = models.ForeignKey(
        "evaluaciones.IntentoEvaluacion",
        on_delete=models.CASCADE,
        related_name="recomendaciones",
    )

    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.GENERAL,
    )

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    prioridad = models.CharField(
        max_length=10,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA,
    )

    tema = models.ForeignKey(
        "academico.Tema",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recomendaciones",
    )

    habilidad = models.ForeignKey(
        "academico.Habilidad",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recomendaciones",
    )

    porcentaje_referencia = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recomendación"
        verbose_name_plural = "Recomendaciones"
        ordering = ["-fecha_creacion", "prioridad"]

    def __str__(self):
        return f"{self.titulo} - {self.estudiante.username}"
