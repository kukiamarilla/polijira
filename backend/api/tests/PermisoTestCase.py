from django.test import TestCase
from django.test import Client
from backend.api.models import Usuario


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
        test_listar_permisos Prueba el listado de todos los permisos
        """
        print("\nProbando listar los permisos.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(isinstance(body, list), True)

    def test_listar_permisos_sin_permiso(self):
        """
        test_listar_permisos_sin_permiso Prueba el listado de todos los permisos
        con un usuario sin permiso para realizar la acción
        """
        print("\nProbando listar los permisos sin permiso.")
        rol = Usuario.objects.get(nombre="testing").rol
        permiso = rol.permisos.get(codigo="ver_permisos")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['ver_permisos'])
