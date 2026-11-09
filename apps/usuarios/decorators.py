
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from apps.usuarios.models import Usuario


def requiere_docente(vista):
    """
    Permite el acceso únicamente a usuarios con rol docente.
    No concede acceso por ser administrador, staff o superusuario.
    """

    @wraps(vista)
    def vista_protegida(request, *args, **kwargs):

        if not request.user.is_authenticated:
            raise PermissionDenied(
                "Debes iniciar sesión para acceder a esta sección."
            )

        if (
            request.user.rol != Usuario.Rol.DOCENTE
            or request.user.is_staff
            or request.user.is_superuser
        ):
            raise PermissionDenied(
                "Esta sección está disponible únicamente para docentes."
            )

        return vista(request, *args, **kwargs)

    return vista_protegida
