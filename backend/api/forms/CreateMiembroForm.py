import json
from django.core.exceptions import ValidationError
from backend.api.models import Proyecto, RolProyecto, Usuario, Miembro
from django import forms


class CreateMiembroForm(forms.Form):
    """
    CreateMiembroForm Valida los datos del request.data al crear un miembro

    Args:
        forms (Form): Form de django

    Atributes:
        usuario (IntegerField): Campo para validar que exista el usuario
        proyecto (IntegerField): Campo para validar que exista el proyecto
        rol (IntegerField): Campo para validar que exista el rol
        horario (CharField): Campo para validar las horas del horario

    """
    usuario = forms.IntegerField(
        min_value=1,
        error_messages={
            "required": "No especificaste el usuario"
        }
    )
    proyecto = forms.IntegerField(
        min_value=1,
        error_messages={
            "required": "No especificaste el proyecto"
        }
    )
    rol = forms.IntegerField(
        min_value=1,
        error_messages={
            "required": "No especificaste el rol"
        }
    )
    horario = forms.CharField(
        error_messages={
            "required": "No especificaste el horario"
        }
    )

    miembro = forms.IntegerField(
        required=False
    )

    def clean_usuario(self):
        """
        clean_usuario Valida que la id de usuario exista en la BD

        Raises:
            ValidationError: Error de Validación

        Returns:
            int: id de usuario
        """
        try:
            cleaned_data = super().clean()
            id = cleaned_data.get("usuario")
            Usuario.objects.get(pk=id)
            return id
        except Usuario.DoesNotExist:
            raise ValidationError("No se encontro un usuario en la base de datos")

    def clean_proyecto(self):
        """
        clean_proyecto Valida que la id de proyecto exista en la BD

        Raises:
            ValidationError: Error de validación

        Returns:
            int: id de proyecto
        """
        try:
            cleaned_data = super().clean()
            id = cleaned_data.get("proyecto")
            Proyecto.objects.get(pk=id)
            return id
        except Proyecto.DoesNotExist:
            raise ValidationError("No se encontro un proyecto en la base de datos")

    def clean_rol(self):
        """
        clean_rol Valida que la id de rol exista en la BD

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
            raise ValidationError("No se encontro un rol en la base de datos")

    def clean_horario(self):
        """
        clean_horario Valida que el horario tenga horas válidas

        Raises:
            ValidationError: Error de validación

        Returns:
            dict: diccionario de dias y horas trabajadas
        """
        cleaned_data = super().clean()
        horario = cleaned_data.get("horario")
        horario = horario.replace("\'", "\"").replace("True", "true").replace("False", "false")
        horario = json.loads(horario)
        for hora in horario.values():
            if not (hora >= 0 and hora <= 24):
                raise ValidationError("No especificaste una hora válida")
        return horario

    def clean_miembro(self):
        """
        clean_miembro_existente Valida que ya no exista el miembro
        """
        cleaned_data = super().clean()
        usuario = cleaned_data.get("usuario")
        proyecto = cleaned_data.get("proyecto")
        rol = cleaned_data.get("rol")
        miembro = Miembro.objects.filter(usuario=usuario, proyecto=proyecto)
        if len(miembro) > 0:
            raise ValidationError("Ya existe el miembro")
