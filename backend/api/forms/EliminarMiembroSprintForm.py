from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import MiembroSprint


class EliminarMiembroSprintForm(forms.Form):
    """
    EliminarMiembroSprintForm Valida si la consulta de eliminar miembro sprint es correcta

    Raises:
        ValidationError: Si no pasaron las validaciones
    """
    miembro_sprint = forms.IntegerField(
        required=True,
        error_messages={
            "required": "No especificaste el miembro sprint"
        }
    )

    def clean_miembro_sprint(self):
        cleaned_data = super().clean()
        id = cleaned_data.get("miembro_sprint")
        try:
            MiembroSprint.objects.get(pk=id)
        except MiembroSprint.DoesNotExist:
            raise ValidationError("No existe el miembro sprint en la base de datos")
