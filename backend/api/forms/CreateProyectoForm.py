import datetime
from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import Proyecto


class CreateProyectoForm(forms.Form):
    """
    CreateProyectoForm Valida si la consulta de crear proyecto es correcta

    Raises:
        ValidationError: Si no se pasaron las validaciones
    """
    nombre = forms.CharField(
        max_length=255,
        empty_value='',
        required=True,
        error_messages={
            "required": "No se especificó ningun nombre",
            "max_length": "Sobrepasó el limite de caracteres"
        }
    )
    fecha_inicio = forms.DateField(
        required=True,
        error_messages={
            "required": "No se especificó ninguna fecha de inicio",
            "invalid": "Fecha inválida"
        }
    )
    fecha_fin = forms.DateField(
        required=True,
        error_messages={
            "required": "No se especificó ninguna fecha de fin",
            "invalid": "Fecha inválida"
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

    def clean_nombre(self):
        """
        clean_nombre Valida que el nombre del proyecto sea unico
        Raises:
            ValidationError: Error de validacion si no se encuentra el proyecto
        """
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        proyecto = Proyecto.objects.filter(nombre=nombre)
        if len(proyecto) > 0:
            raise ValidationError("Ya existe un proyecto con ese nombre")
        return nombre
