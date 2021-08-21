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
        self._client = Client()

    def test_listar_usuario(self):
        """
        test_listar_usuario Prueba listar todos los usuarios
        """
        print("\nProbando listar todos los usuarios")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.get("/api/usuarios/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(body), Usuario.objects.count())

    def test_obtener_usuario(self):
        """
        test_obtener_usuario Prueba obtener un usuario
        """
        print("\nProbando obtener un usuario")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.get("/api/usuarios/1/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body['id'], 1)
