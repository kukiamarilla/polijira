from django import forms


class ResponderEstimacionForm(forms.Form):
    horas_estimadas = forms.IntegerField(
        min_value=0,
        error_messages={
            "required": "No se especificó ninguna hora estimada",
            "min_value": "La hora no puede ser negativa"
        }
    )
