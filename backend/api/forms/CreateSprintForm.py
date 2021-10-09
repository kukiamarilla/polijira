from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import Proyecto


class CreateSprintForm(forms.Form):
    fecha_inicio = forms.DateField(
        error_messages={
            "required": "El campo fecha de inicio es obligatorio"
        }
    )
    fecha_fin = forms.DateField(
        error_messages={
            "required": "El campo fecha de fin es obligatorio"
        }
    )
    capacidad = forms.IntegerField(
        min_value=0,
        error_messages={
            "required": "El campo capacidad es obligatorio",
            "min_value": "La capacidad no puede ser negativa"
        }
    )
    proyecto = forms.IntegerField(
        error_messages={
            "required": "No se especificó ningún proyecto"
        }
    )

    def clean_proyecto(self):
        """
        clean_proyecto Valida si existe el proyecto en la BD
        """
        try:
            cleaned_data = super().clean()
            proyecto = cleaned_data.get("proyecto")
            Proyecto.objects.get(pk=proyecto)
            return proyecto
        except Proyecto.DoesNotExist:
            raise ValidationError("No se encontró un Proyecto en la base de datos")

    def clean_fecha_inicio(self):
        """
        clean_fecha_inicio Valida que esta fecha no esté en el pasado
        """
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        if fecha_inicio < date.today():
            raise ValidationError("La fecha de inicio no puede estar en el pasado")
        return fecha_inicio

    def clean_fecha_fin(self):
        """
        clean_fecha_fin Valida que la fecha de fin no sea menor a la de inicio
        """
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        if fecha_fin and fecha_inicio:
            if fecha_fin < fecha_inicio:
                raise ValidationError("La fecha de fin no puede ser menor a la de inicio")
        return fecha_fin
