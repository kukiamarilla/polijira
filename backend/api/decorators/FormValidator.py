from functools import wraps
from rest_framework import status
from rest_framework.response import Response


class FormValidator():
    """
    FormValidator Decorador para la lógica de validacion de los views

    Args:
        fn (function): View a decorar
        form(forms.Form): Form a utilizar para la validación

    Returns:
        Response: Error HTTP 422 si no se pasan las validaciones o le respuesta del view en caso contrario
    """

    def __init__(self, form=None):
        self.form_cls = form

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            form = self.form_cls(args[1].data)
            if not form.is_valid():
                response = {"message": "Error de validación", "errors": form.errors}
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return fn(*args, **kwargs)
        return wrapper
