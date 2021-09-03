from django import forms


class CreateRolForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        required=True
    )
