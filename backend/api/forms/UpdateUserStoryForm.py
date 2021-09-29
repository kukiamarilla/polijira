from django import forms
from django.core.exceptions import ValidationError


class UpdateUserStoryForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        error_messages={
            "required": "No se especificó ningún nombre",
            "max_length": "Superó el límite máximo de longitud para el nombre"
        }
    )
    descripcion = forms.CharField(
        error_messages={
            "required": "No se especificó ninguna descripción"
        }
    )
    horas_estimadas = forms.IntegerField(
        min_value=1,
        error_messages={
            "required": "No se especificó ninguna hora estimada",
            "min_value": "La hora no puede ser negativa"
        }
    )
    prioridad = forms.IntegerField(
        max_value=10,
        min_value=1,
        error_messages={
            "required": "No se especificó ninguna prioridad",
            "max_value": "La prioridad solo puede ser máximo 10",
            "min_value": "La prioridad solo puede ser mínimo 1"
        }
    )
    estado_estimacion = forms.CharField(
        max_length=1,
        error_messages={
            "required": "No se especificó ningún estado de estimación",
            "max_length": "El estado estimacion debe tener un caracter.(N) No estimado,(P) Parcial,(C) Completo"
        }
    )

    def clean_estado_estimacion(self):
        cleaned_data = super().clean()
        estado_estimacion = cleaned_data.get("estado_estimacion")
        if not estado_estimacion == "N" and \
           not estado_estimacion == "P" and \
           not estado_estimacion == "C":
            raise ValidationError("El estado de estimación solo puede ser N, P, C\nNo estimado, Parcial, Completo")
        return estado_estimacion