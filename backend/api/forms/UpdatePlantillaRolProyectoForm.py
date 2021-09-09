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
