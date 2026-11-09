
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

from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from .models import Evaluacion, Pregunta, OpcionRespuesta


# Formulario para crear y editar preguntas.
class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = [
            "enunciado",
            "tema",
            "habilidades",
            "puntaje",
            "orden",
            "es_provisional",
            "activa",
        ]

        labels = {
            "enunciado": "Enunciado de la pregunta",
            "tema": "Tema relacionado",
            "habilidades": "Habilidades que evalúa",
            "puntaje": "Puntaje",
            "orden": "Orden de la pregunta",
            "es_provisional": "¿Es una pregunta provisional?",
            "activa": "¿Está activa?",
        }

        widgets = {
            "enunciado": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Escribe el enunciado de la pregunta",
            }),
            "tema": forms.Select(attrs={
                "class": "form-control",
            }),
            "habilidades": forms.SelectMultiple(attrs={
                "class": "form-control",
            }),
            "puntaje": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1",
            }),
            "orden": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1",
            }),
            "es_provisional": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
            "activa": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }


# Formulario individual para cada opción de respuesta.
class OpcionRespuestaForm(forms.ModelForm):
    class Meta:
        model = OpcionRespuesta
        fields = [
            "texto",
            "es_correcta",
            "orden",
        ]

        labels = {
            "texto": "Texto de la opción",
            "es_correcta": "¿Es la respuesta correcta?",
            "orden": "Orden de la opción",
        }

        widgets = {
            "texto": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Escribe una opción de respuesta",
            }),
            "es_correcta": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
            "orden": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1",
            }),
        }


# Validación de las opciones de respuesta.
class BaseOpcionRespuestaFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()

        if any(self.errors):
            return

        opciones_validas = []

        for form in self.forms:
            if not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE", False):
                continue

            texto = form.cleaned_data.get("texto")

            if texto:
                opciones_validas.append(form.cleaned_data)

        if len(opciones_validas) < 2:
            raise forms.ValidationError(
                "Debes registrar al menos dos opciones de respuesta."
            )

        correctas = [
            opcion for opcion in opciones_validas
            if opcion.get("es_correcta")
        ]

        if len(correctas) != 1:
            raise forms.ValidationError(
                "Debes marcar exactamente una opción como correcta."
            )


OpcionRespuestaFormSet = inlineformset_factory(
    Pregunta,
    OpcionRespuesta,
    form=OpcionRespuestaForm,
    formset=BaseOpcionRespuestaFormSet,
    extra=4,
    min_num=2,
    validate_min=True,
    can_delete=True,
)
