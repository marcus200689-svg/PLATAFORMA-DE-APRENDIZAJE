
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuario de la plataforma de aprendizaje.
    Django administra la autenticación y las contraseñas.
    """

    class Rol(models.TextChoices):
        ESTUDIANTE = "estudiante", "Estudiante"
        DOCENTE = "docente", "Docente"
        ADMINISTRADOR = "administrador", "Administrador"

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.ESTUDIANTE,
    )

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

class Docente(Usuario):
    class Meta:
        proxy = True
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"


class Estudiante(Usuario):
    class Meta:
        proxy = True
        verbose_name = "Alumno registrado"
        verbose_name_plural = "Alumnos registrados"