from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import Miembro


class CreateUserStoryForm(forms.Form):
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
            "min_value": "La hora solo puede ser como mínimo 1"
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
    desarrollador = forms.IntegerField(
        error_messages={
            "required": "No se especificó ningún desarrollador"
        }
    )
    estado_estimacion = forms.CharField(
        max_length=1,
        error_messages={
            "required": "No se especificó ningún estado de estimación",
            "max_length": "Solo puedes indicar el estado estimación con 'N', 'P', 'C' \n No estimado, Parcial, Completo"
        }
    )

    def clean_desarrollador(self):
        try:
            cleaned_data = super().clean()
            desarrollador_id = cleaned_data.get("desarrollador")
            Miembro.objects.get(pk=desarrollador_id)
            return desarrollador_id
        except Miembro.DoesNotExist:
            raise ValidationError("No se encontró el desarrollador en la base de datos")
