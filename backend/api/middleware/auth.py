import re
import os
import json
import time
import logging
from rest_framework.exceptions import (
    PermissionDenied,
    AuthenticationFailed,
    NotAuthenticated,
)
from django.conf import settings
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from backend.api.models import Usuario
import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin._token_gen import ExpiredIdTokenError
from firebase_admin._auth_utils import InvalidIdTokenError

logger = logging.getLogger(__name__)


class AuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        """Constructor del AuthMiddleware

        Args:
            get_response (callable): Obtiene la respuesta de la consulta a ejecutar
        """
        self.get_response = get_response
        cred = credentials.Certificate(settings.FIREBASE_CONFIG)
        try:
            firebase_admin.get_app()
        except:
            firebase_admin.initialize_app(cred)

    def __call__(self, request):
        """
        :param request:
        :return:
        """
        if request.user.is_authenticated:
            return self.get_response(request)

        if not ("Authorization" in request.headers):
            return JsonResponse(
                {
                    "message": "Debe autenticarse para realizar esta acción",
                    "error": "unauthenticated"
                },
                status=PermissionDenied.status_code,
            )

        authorization = request.headers["Authorization"].split(" ")
        if len(authorization) != 2:
            return JsonResponse(
                {
                    "message": "Debe autenticarse para realizar esta acción",
                    "error": "unauthenticated"
                },
                status=PermissionDenied.status_code,
            )
        if authorization[0] != "JWT":
            return JsonResponse(
                {
                    "message": "Debe autenticarse para realizar esta acción",
                    "error": "unauthenticated"
                },
                status=PermissionDenied.status_code,
            )
        token = authorization[1]
        try:
            userinfo = auth.verify_id_token(token)
            usuario = Usuario.objects.filter(firebase_uid=userinfo["uid"])
            if usuario.count() == 0:
                usuario = Usuario.objects.create(
                    nombre=userinfo["name"],
                    email=userinfo["email"],
                    estado="I",
                    firebase_uid=userinfo["uid"]
                )
                usuario.save()
            else:
                usuario = usuario[0]
                if usuario.estado == "I":
                    return JsonResponse(
                        {
                            "message": "Su usuario aún no fue activado, debe esperar la confirmación del administrador",
                            "error": "unauthenticated"
                        },
                        status=PermissionDenied.status_code,
                    )
            request._force_auth_user = usuario
        except ExpiredIdTokenError:
            return JsonResponse(
                {
                    "message": "Su sesión ha expirado",
                    "error": "unauthenticated"
                },
                status=AuthenticationFailed.status_code,
            )
        except InvalidIdTokenError:
            return JsonResponse(
                {
                    "message": "Debe autenticarse para realizar esta acción",
                    "error": "unauthenticated"
                },
                status=NotAuthenticated.status_code,
            )
        return self.get_response(request)
