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
    sprint = forms.IntegerField(
        min_value=1,
        error_messages={
            "required": "No especificaste el sprint"
        }
    )
    miembro = forms.IntegerField(
        min_value=1,
        error_messages={
            "required": "No especificaste el miembro"
        }
    )

    miembro_sprint = forms.IntegerField(
        required=False
    )

    def clean_sprint(self):
        """
        clean_sprint Valida que la id de sprint exista en la BD

        Raises:
            ValidationError: Error de validación

        Returns:
            int: id de sprint
        """
        try:
            cleaned_data = super().clean()
            id = cleaned_data.get("sprint")
            Sprint.objects.get(pk=id)
            return id
        except Sprint.DoesNotExist:
            raise ValidationError("No se encontro un sprint en la base de datos")

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
            miembro_id = cleaned_data.get("miembro")
            sprint_id = cleaned_data.get("sprint")
            miembro = Miembro.objects.get(pk=miembro_id)
            sprint = Sprint.objects.get(pk=sprint_id)
            if miembro.proyecto != sprint.proyecto:
                # el miembro y el sprint no son del mismo proyecto
                raise ValidationError("El miembro no pertenece a este proyecto")
            return miembro_id
        except Miembro.DoesNotExist:
            raise ValidationError("No se encontro un miembro en la base de datos")
        except Sprint.DoesNotExist:
            raise ValidationError("El miembro no pertenece a este proyecto:)")

    def clean_miembro_sprint(self):
        """
        clean_miembro_sprint Valida que ya no exista el miembro en el sprint
        """
        cleaned_data = super().clean()
        miembro = cleaned_data.get("miembro")
        sprint = cleaned_data.get("sprint")
        miembro_sprint = MiembroSprint.objects.filter(miembro_proyecto=miembro, sprint=sprint)
        if len(miembro_sprint) > 0:
            raise ValidationError("Ya existe el miembro")
