from backend.api.models.Permiso import Permiso
from django.test import TestCase
from django.test import Client


class PermisoTestCase(TestCase):
    """
    PermisoTestCase prueba las funcionalidades de Permisos
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
    ]

    def setUp(self):
        """
        setUp Configura el testcase
        """
        self.client = Client()

    def test_listar_permisos(self):
        print("\nProbando listado de permisos.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(isinstance(body, list), True)
