import datetime
from django import forms
from django.core.exceptions import ValidationError


class CreateProyectoForm(forms.Form):
    nombre = forms.CharField(max_length=255, empty_value='', required=True)
    fecha_inicio = forms.DateField(required=True)
    fecha_fin = forms.DateField(required=True)
    estado = forms.CharField(max_length=1, required=False)

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data['fecha_inicio']
        if fecha_inicio < datetime.date.today():
            raise ValidationError("No puede estar en el pasado")
