from django.db import models


class Materia(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
    )
    descripcion = models.TextField(
        blank=True,
    )
    activa = models.BooleanField(
        default=True,
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Tema(models.Model):
    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name="temas",
    )
    nombre = models.CharField(
        max_length=100,
    )
    descripcion = models.TextField(
        blank=True,
    )
    activo = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Tema"
        verbose_name_plural = "Temas"
        ordering = ["materia__nombre", "nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["materia", "nombre"],
                name="tema_nombre_unico_por_materia",
            ),
        ]

    def __str__(self):
        return f"{self.materia.nombre} - {self.nombre}"


class Habilidad(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
    )
    descripcion = models.TextField(
        blank=True,
    )
    activa = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre