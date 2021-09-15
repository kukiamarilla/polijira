from django import forms
from django.core.exceptions import ValidationError
from backend.api.models import PermisoProyecto


class EliminarPermisoProyectoForm(forms.Form):
    """
    EliminarPermisoRolForm Valida si la consulta de eliminar permiso a Plantilla de Rol de Proyecto es correcta

    Raises:
        ValidationError: Si no pasaron las validaciones
    """
    id = forms.IntegerField(
        required=True,
        error_messages={
            "required": "No se pasó ninguna id de Permiso"
        }
    )

    def clean_id(self):
        cleaned_data = super().clean()
        id = cleaned_data.get("id")
        try:
            PermisoProyecto.objects.get(pk=id)
        except PermisoProyecto.DoesNotExist:
            raise ValidationError("No existe el permiso en la base de datos")
