
from django import forms

from .models import Evaluacion


class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = [
            "titulo",
            "descripcion",
            "materia",
            "activa",
        ]

        labels = {
            "titulo": "Título de la evaluación",
            "descripcion": "Descripción",
            "materia": "Materia",
            "activa": "¿Está activa?",
        }

        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Evaluación de Matemáticas",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe el propósito de la evaluación",
                    "rows": 4,
                }
            ),
            "materia": forms.Select(
                attrs={"class": "form-control"}
            ),
            "activa": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
