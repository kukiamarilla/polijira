from django.test import TestCase
from django.test import Client


class PermisoTestCase(TestCase):
    """
    PermisoTestCase Prueba las funcionalidades de Permisos
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
        "backend/api/fixtures/testing/permisos.json",
        "backend/api/fixtures/testing/roles.json"
    ]

    def setUp(self):
        """
        setUp Configura el testcase
        """
        self.client = Client()

    def test_listar_permisos(self):
        """
        test_listar_permisos Prueba el listado todos los permisos
        """
        print("\nProbando listado de permisos.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(isinstance(body, list), True)
