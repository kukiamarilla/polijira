from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import PermisoProyecto


class AgregarPermisoRolProyectoForm(forms.Form):
    """
    AgregarPermisoRolProyectoForm Valida si la consulta de agregar permiso a rol de proyecto es correcta

    Raises:
        ValidationError: Si no se pasaron las validaciones
    """
    id = forms.IntegerField(
        required=True,
        error_messages={
            "required": "No se pasó ninguna id de Permiso de Proyecto"
        }
    )

    def clean_id(self):
        cleaned_data = super().clean()
        id = cleaned_data.get("id")
        try:
            PermisoProyecto.objects.get(pk=id)
        except PermisoProyecto.DoesNotExist:
            raise ValidationError("No existe el permiso de proyecto en la base de datos")
