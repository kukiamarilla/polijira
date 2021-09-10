from django.db import reset_queries
from backend.api.models import Usuario, PlantillaRolProyecto, PermisoProyecto
from django.test import TestCase, Client
from django.db.models import Q


class PlantillaRolProyectoTestCase(TestCase):
    """
    PlantillaRolProyectoTestCase Prueba las funcionalidades de una Plantilla de Rol de Proyecto
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
        "backend/api/fixtures/testing/permisos.json",
        "backend/api/fixtures/testing/roles.json",
        "backend/api/fixtures/testing/permisosProyecto.json",
        "backend/api/fixtures/testing/plantillas.json"
    ]

    def setUp(self):
        """
        setUp Configura el testcase
        """
        self.client = Client()

    def test_listar_plantillas(self):
        """
        test_listar_plantillas Prueba obtener todas las plantillas de rol de proyecto
        """
        print("\nProbando listar plantillas.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/plantillas/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(PlantillaRolProyecto.objects.count(), len(body))

    def test_crear_plantilla(self):
        """
        test_crear_plantilla Prueba crear una plantilla de rol de proyecto 
        """
        print("\nProbando crear una plantilla")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "PlantillaTest",
            "permisos": [
                {"id": 1},
                {"id": 2}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, "application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(body["nombre"], plantilla["nombre"])
        self.assertEquals(body["permisos"][0]["id"], 1)
        self.assertEquals(body["permisos"][1]["id"], 2)

    def test_modificar_plantilla(self):
        """
        test_modificar_plantilla Prueba modificar una plantilla de rol de proyecto
        """
        print("\nProbando crear una plantilla")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "PlantillaModificadoTest"
        }
        response = self.client.put("/api/plantillas/1/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(body["id"], 1)
        self.assertEquals(body["nombre"], plantilla["nombre"])

    def test_eliminar_plantilla(self):
        """
        test_eliminar_plantilla Prueba eliminar una plantilla de rol de proyecto
        """
        print("\nProbando eliminar una plantilla")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/plantillas/1/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(body["message"], "Plantilla de rol Eliminado")

    def test_listar_permisos(self):
        """
        test_listar_permisos Prueba obtener todos los permisos de una plantilla
        """
        print("\nProbando obtener todos los permisos de una plantilla")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/plantillas/1/permisos/")
        self.assertEquals(response.status_code, 200)
        plantilla = PlantillaRolProyecto.objects.get(pk=1)
        permisos = plantilla.permisos.all()
        body = response.json()
        self.assertEquals(len(body), len(permisos))

    def test_agregar_permisos(self):
        """
        test_agregar_permisos Prueba agregar permisos a una plantilla
        """
        print("\nProbando agregar permisos a una plantilla")
        self.client.login(username="testing", password="polijira2021")
        permiso = {"id": 2}
        response = self.client.post("/api/plantillas/1/permisos/", permiso, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        plantilla = PlantillaRolProyecto.objects.get(pk=1)
        self.assertEquals(len(body["permisos"]), plantilla.permisos.count())

    def test_eliminar_permiso(self):
        """
        test_eliminar_permiso Prueba eliminar un permiso a una plantilla
        """
        print("\nProbando eliminar un permiso de una plantilla")
        self.client.login(username="testing", password="polijira2021")
        permiso = {"id": 1}
        response = self.client.delete("/api/plantillas/1/permisos/", permiso, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        plantilla = PlantillaRolProyecto.objects.get(pk=1)
        self.assertEquals(len(body["permisos"]), plantilla.permisos.count())
