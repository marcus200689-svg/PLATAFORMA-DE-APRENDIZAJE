
from django import forms

from apps.academico.models import Materia, Tema, Habilidad


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Nombre de la materia",
            }),
            "descripcion": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Descripción de la materia",
            }),
        }


class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ["materia", "nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Nombre del tema",
            }),
            "descripcion": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Descripción del tema",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["materia"].queryset = Materia.objects.filter(
            activa=True
        ).order_by("nombre")


class HabilidadForm(forms.ModelForm):
    class Meta:
        model = Habilidad
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Nombre de la habilidad",
            }),
            "descripcion": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Descripción de la habilidad",
            }),
        }
