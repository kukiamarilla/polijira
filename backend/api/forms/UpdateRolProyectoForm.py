from django import forms


class UpdateRolProyectoForm(forms.Form):
    """
    UpdateRolProyectoForm Form para validar la modificacion de RolProyecto

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
