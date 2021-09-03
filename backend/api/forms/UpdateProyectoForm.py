import datetime
from django import forms
from django.core.exceptions import ValidationError


class UpdateProyectoForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        required=True,
        error_messages={
            "max_length": "Sobrepasó el limite de caracteres",
            "required": "No se especificó ningun nombre"
        }
    )
    fecha_inicio = forms.DateField(
        required=True,
        error_messages={
            "invalid": "Fecha de inicio inválida",
            "required": "No se especificó ninguna fecha de inicio"
        }
    )
    fecha_fin = forms.DateField(
        required=True,
        error_messages={
            "invalid": "Fecha de fin inválida",
            "required": "No se especificó ninguna fecha de fin"
        }
    )
    estado = forms.CharField(
        max_length=1,
        required=False,
        error_messages={
            "max_length": "El estado solo puede tener un caracter"
        }
    )
    scrum_master_id = forms.IntegerField(
        required=True,
        error_messages={
            "required": "No se especificó el Scrum Master"
        }
    )

    def clean_fecha_inicio(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        if fecha_inicio:
            if fecha_inicio < datetime.date.today():
                raise ValidationError("La fecha de inicio no puede estar en el pasado")
        return fecha_inicio

    def clean_fecha_fin(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise ValidationError("La fecha de fin no puede ser menor a la de inicio")
        return fecha_fin
