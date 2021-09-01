from functools import wraps
from rest_framework import status
from rest_framework.response import Response


class FormValidator():

    def __init__(self, form=None):
        self.form_cls = form

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            form = self.form_cls(args[1].data)
            if not form.is_valid():
                response = {"message": "Error de validación", "errors": form.errors}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            return fn(*args, **kwargs)
        return wrapper
