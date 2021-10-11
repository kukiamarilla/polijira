from django import forms


class UpdateUserStoryForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        error_messages={
            "required": "Falta especificar un nombre o dejar con su valor actual",
            "max_length": "Superó el límite máximo de longitud para el nombre"
        }
    )
    descripcion = forms.CharField(
        error_messages={
            "required": "Falta especificar una descripción o dejar con su valor actual"
        }
    )
    prioridad = forms.IntegerField(
        max_value=10,
        min_value=1,
        error_messages={
            "required": "Falta especificar la prioridad o dejar con su valor actual",
            "max_value": "La prioridad solo puede ser máximo 10",
            "min_value": "La prioridad solo puede ser mínimo 1"
        }
    )
