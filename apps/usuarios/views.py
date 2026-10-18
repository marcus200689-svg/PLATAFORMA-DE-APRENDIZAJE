
from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Página principal
def inicio(request):
    return render(request, "inicio.html")


# Registro de usuarios
def registro(request):
    return render(request, "usuarios/registro.html")


# Inicio de sesión
def iniciar_sesion(request):
    return render(request, "usuarios/login.html")


# Perfil del usuario
def perfil(request):
    return render(request, "usuarios/perfil.html")


# Cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect("inicio")
