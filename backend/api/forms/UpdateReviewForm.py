from django import forms


class UpdateReviewForm(forms.Form):
    """
    UpdateReviewForm Valida los datos del request.data al modificar un review

    Args:
        forms (Form): Form de django

    Atributes:
        observacion (TextField): Campo para validar que se especifca la observacion
    """

    observacion = forms.CharField(
        required=True,
        error_messages={
            "required": "No especificaste la observacion"
        }
    )
