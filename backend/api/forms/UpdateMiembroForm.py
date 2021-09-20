from django.core.exceptions import ValidationError
from backend.api.models import RolProyecto
from django import forms


class UpdateMiembroForm(forms.Form):
    """
    UpdateMiembroForm Valida los datos de request.data al modificar miembro

    Args:
        forms (Form): Form de django

    Atributes:
        rol (IntegerField): Campo para validar que exista el rol
    """
    rol = forms.IntegerField(
        min_value=1,
        error_messages={
            "required": "No especificaste el rol"
        }
    )

    def clean_rol(self):
        """
        clean_rol Valida si la id de rol existe en la BD

        Raises:
            ValidationError: Error de validación

        Returns:
            int: id de rol
        """
        try:
            cleaned_data = super().clean()
            id = cleaned_data.get("rol")
            RolProyecto.objects.get(pk=id)
            return id
        except RolProyecto.DoesNotExist:
            raise ValidationError("No se encontró un rol en la base de datos")
