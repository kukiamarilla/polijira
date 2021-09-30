from django import forms
from django.core.exceptions import ValidationError


class UpdateHorarioForm(forms.Form):
    """
    UpdateHorarioForm Valida que el horario tenga un rango de 0 a 24 horas

    Args:
        forms (Form): Form del módulo django
    """
    lunes = forms.IntegerField(
        max_value=24,
        error_messages={
            "max_value": "Un dia no puede tener mas de 24 horas"
        }
    )
    martes = forms.IntegerField(
        max_value=24,
        error_messages={
            "max_value": "Un dia no puede tener mas de 24 horas"
        }
    )
    miercoles = forms.IntegerField(
        max_value=24,
        error_messages={
            "max_value": "Un dia no puede tener mas de 24 horas"
        }
    )
    jueves = forms.IntegerField(
        max_value=24,
        error_messages={
            "max_value": "Un dia no puede tener mas de 24 horas"
        }
    )
    viernes = forms.IntegerField(
        max_value=24,
        error_messages={
            "max_value": "Un dia no puede tener mas de 24 horas"
        }
    )
    sabado = forms.IntegerField(
        max_value=24,
        error_messages={
            "max_value": "Un dia no puede tener mas de 24 horas"
        }
    )
    domingo = forms.IntegerField(
        max_value=24,
        error_messages={
            "max_value": "Un dia no puede tener mas de 24 horas"
        }
    )

    def clean_lunes(self):
        cleaned_data = super().clean()
        lunes = cleaned_data.get("lunes")
        if lunes < 0:
            raise ValidationError("La hora no puede ser menor a cero")
        return lunes

    def clean_martes(self):
        cleaned_data = super().clean()
        martes = cleaned_data.get("martes")
        if martes < 0:
            raise ValidationError("La hora no puede ser menor a cero")
        return martes

    def clean_miercoles(self):
        cleaned_data = super().clean()
        miercoles = cleaned_data.get("miercoles")
        if miercoles < 0:
            raise ValidationError("La hora no puede ser menor a cero")
        return miercoles

    def clean_jueves(self):
        cleaned_data = super().clean()
        jueves = cleaned_data.get("jueves")
        if jueves < 0:
            raise ValidationError("La hora no puede ser menor a cero")
        return jueves

    def clean_viernes(self):
        cleaned_data = super().clean()
        viernes = cleaned_data.get("viernes")
        if viernes < 0:
            raise ValidationError("La hora no puede ser menor a cero")
        return viernes

    def clean_sabado(self):
        cleaned_data = super().clean()
        sabado = cleaned_data.get("sabado")
        if sabado < 0:
            raise ValidationError("La hora no puede ser menor a cero")
        return sabado

    def clean_domingo(self):
        cleaned_data = super().clean()
        domingo = cleaned_data.get("domingo")
        if domingo < 0:
            raise ValidationError("La hora no puede ser menor a cero")
        return domingo
