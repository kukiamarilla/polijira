import json
from django.core.exceptions import ValidationError
from backend.api.models import Miembro, Sprint
from django import forms

from backend.api.models.MiembroSprint import MiembroSprint


class CreateMiembroSprintForm(forms.Form):
    """
    CreateMiembroSprintForm Valida los datos del request.data al crear un miembro del sprint

    Args:
        forms (Form): Form de django

    Atributes:
        miembro (IntegerField): Campo para validar que exista el miembro
        sprint (IntegerField): Campo para validar que exista el sprint
    """
    miembro = forms.IntegerField(
        min_value=1,
        error_messages={
            "required": "No especificaste el miembro"
        }
    )

    def clean_miembro(self):
        """
        clean_miembro Valida que la id de miembro exista en la BD

        Raises:
            ValidationError: Error de Validación

        Returns:
            int: id de miembro
        """
        try:
            cleaned_data = super().clean()
            id = cleaned_data.get("miembro")
            Miembro.objects.get(pk=id)
            return id
        except Miembro.DoesNotExist:
            raise ValidationError("No se encontro un miembro en la base de datos")
