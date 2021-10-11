from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import Proyecto


class CreateUserStoryForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        error_messages={
            "required": "El User Story no puede estar sin nombre",
            "max_length": "Superó el límite máximo de longitud para el nombre"
        }
    )
    prioridad = forms.IntegerField(
        max_value=10,
        min_value=1,
        error_messages={
            "max_value": "La prioridad solo puede ser máximo 10",
            "min_value": "La prioridad solo puede ser mínimo 1"
        }
    )
    proyecto = forms.IntegerField(
        error_messages={
            "required": "No se ha especificado ningún proyecto"
        }
    )

    def clean_proyecto(self):
        try:
            cleaned_data = super().clean()
            proyecto_id = cleaned_data.get("proyecto")
            Proyecto.objects.get(pk=proyecto_id)
            return proyecto_id
        except Proyecto.DoesNotExist:
            raise ValidationError("No se encontró el proyecto en la base de datos")
