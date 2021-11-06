from django import forms


class UpdateActividadForm(forms.Form):
    """
    UpdateActividadForm Valida los datos enviados al Modificar Actividad

    Args:
        forms (Form): Form del módulo django
    """
    descripcion = forms.CharField(
        error_messages={
            "required": "No se pasó: Descripcion"
        }
    )
    horas = forms.IntegerField(
        min_value=0,
        error_messages={
            "required": "No se pasó: Horas",
            "min_value": "La hora no puede ser negativa"
        }
    )
