from django.core.exceptions import ValidationError
from backend.api.models import PlantillaRolProyecto
from django import forms


class UpdatePlantillaRolProyectoForm(forms.Form):
    """
    UpdateRolForm Form para validar la modificacion de PlantillaRolProyecto

    Args:
        forms (Form): Form de django
    """
    nombre = forms.CharField(
        max_length=255,
        required=True,
        error_messages={
            "required": "No se especificó ningun nombre",
            "max_length": "El nombre superó el máximo número de caracteres"
        }
    )

    def clean_nombre(self):
        """
        clean_nombre Valida que no se cree dos plantillas con el mismo nombre

        Raises:
            ValidationError: Error de validación

        Returns:
            str: Nombre de la plantilla
        """
        try:
            cleaned_data = super().clean()
            nombre = cleaned_data.get("nombre")
            PlantillaRolProyecto.objects.get(nombre=nombre)
            raise ValidationError("No puede existir dos plantillas con el mismo nombre")
        except PlantillaRolProyecto.DoesNotExist:
            return nombre
