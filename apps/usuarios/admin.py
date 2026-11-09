
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Docente, Estudiante


class UsuarioAdminBase(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "rol",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        ("Información académica", {"fields": ("rol",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Información académica", {"fields": ("rol",)}),
    )


@admin.register(Usuario)
class UsuarioAdmin(UsuarioAdminBase):
    list_filter = ("rol", "is_active", "is_staff")


@admin.register(Docente)
class DocenteAdmin(UsuarioAdminBase):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
    )

    list_filter = ("is_active",)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            rol=Usuario.Rol.DOCENTE
        )

    def save_model(self, request, obj, form, change):
        obj.rol = Usuario.Rol.DOCENTE
        obj.is_staff = False
        obj.is_superuser = False
        super().save_model(request, obj, form, change)
        
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["rol"] = Usuario.Rol.DOCENTE
        return initial


@admin.register(Estudiante)
class EstudianteAdmin(UsuarioAdminBase):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
    )

    list_filter = ("is_active",)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            rol=Usuario.Rol.ESTUDIANTE
        )

    def has_add_permission(self, request):
        return False
