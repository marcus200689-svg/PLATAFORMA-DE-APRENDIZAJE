
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.usuarios.models import Usuario


def inicio(request):
    return render(request, "inicio.html")


def registro(request):
    errores = []

    if request.method == "POST":
        nombre = request.POST.get("first_name", "").strip()
        apellidos = request.POST.get("last_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        # Validar nombre y apellidos.
        if not nombre:
            errores.append("El nombre es obligatorio.")

        if not apellidos:
            errores.append("Los apellidos son obligatorios.")

        # Validar nombre de usuario.
        if not username:
            errores.append("El nombre de usuario es obligatorio.")
        elif Usuario.objects.filter(username__iexact=username).exists():
            errores.append("Ese nombre de usuario ya está registrado.")

        # Validar correo electrónico.
        if not email:
            errores.append("El correo electrónico es obligatorio.")
        elif Usuario.objects.filter(email__iexact=email).exists():
            errores.append("Ese correo electrónico ya está registrado.")

        # Validar contraseñas.
        if not password:
            errores.append("La contraseña es obligatoria.")

        if password != password_confirm:
            errores.append("Las contraseñas no coinciden.")

        if password:
            try:
                validate_password(password)
            except ValidationError as excepcion:
                errores.extend(excepcion.messages)

        # Crear siempre una cuenta de estudiante.
        # El rol no se obtiene del formulario ni de los datos POST.
        if not errores:
            Usuario.objects.create_user(
                username=username,
                email=email,
                first_name=nombre,
                last_name=apellidos,
                password=password,
                rol=Usuario.Rol.ESTUDIANTE,
            )

            messages.success(
                request,
                "Tu cuenta se creó correctamente. Ya puedes iniciar sesión."
            )
            return redirect("usuarios:login")

    return render(
        request,
        "usuarios/registro.html",
        {"errores": errores},
    )


def iniciar_sesion(request):
    rol_solicitado = ""

    if request.method == "POST":
        rol_solicitado = request.POST.get("rol", "").strip()

    roles_validos = [
        Usuario.Rol.ESTUDIANTE,
        Usuario.Rol.DOCENTE,
        Usuario.Rol.ADMINISTRADOR,
    ]

    formulario = AuthenticationForm(
        request,
        data=request.POST if request.method == "POST" else None,
    )

    formulario.fields["username"].widget.attrs.update({
        "class": "campo-input",
        "placeholder": "Escribe tu nombre de usuario",
        "autocomplete": "username",
    })

    formulario.fields["password"].widget.attrs.update({
        "class": "campo-input",
        "placeholder": "Escribe tu contraseña",
        "autocomplete": "current-password",
    })

    if request.method == "POST":
        if rol_solicitado not in roles_validos:
            messages.error(
                request,
                "Selecciona un tipo de usuario válido."
            )

        elif formulario.is_valid():
            usuario = formulario.get_user()

            # Un superusuario siempre puede ingresar como administrador.
            es_administrador = (
                usuario.is_superuser
                or (
                    usuario.rol == Usuario.Rol.ADMINISTRADOR
                    and usuario.is_staff
                )
            )

            acceso_correcto = False

            if rol_solicitado == Usuario.Rol.ESTUDIANTE:
                acceso_correcto = (
                    usuario.rol == Usuario.Rol.ESTUDIANTE
                    and not usuario.is_staff
                    and not usuario.is_superuser
                )

            elif rol_solicitado == Usuario.Rol.DOCENTE:
                acceso_correcto = (
                    usuario.rol == Usuario.Rol.DOCENTE
                    and not usuario.is_staff
                    and not usuario.is_superuser
                )

            elif rol_solicitado == Usuario.Rol.ADMINISTRADOR:
                acceso_correcto = es_administrador

            if not acceso_correcto:
                messages.error(
                    request,
                    "Tu cuenta no tiene permisos para ingresar "
                    "con el tipo de usuario seleccionado."
                )
            else:
                login(request, usuario)

                if es_administrador:
                    return redirect("admin:index")

                if usuario.rol == Usuario.Rol.DOCENTE:
                    return redirect("evaluaciones:profesor_lista")

                return redirect("inicio")

    return render(
        request,
        "usuarios/login.html",
        {
            "formulario": formulario,
            "rol_solicitado": rol_solicitado,
        },
    )


@login_required
def perfil(request):
    return render(request, "usuarios/perfil.html")


@require_POST
def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("usuarios:login")
