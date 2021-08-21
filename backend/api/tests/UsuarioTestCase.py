from backend.api.models.Usuario import Usuario
from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.contrib.auth.models import User
import requests


class UsuarioTestCase(TestCase):
    """
    UsuarioTestCase Prueba las funcionalidades del modelo Usuario
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
    ]

    def setUp(self):
        """
        setUp Configura el TestCase
        """
        self.client = Client()
