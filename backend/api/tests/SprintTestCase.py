from datetime import date
from django.test import TestCase, Client
from backend.api.models import MiembroSprint, SprintBacklog, ProductBacklog, Sprint, Usuario, Miembro, Proyecto, RegistroUserStory, UserStory, PermisoProyecto
from backend.api.serializers import SprintSerializer


class SprintTestCase(TestCase):
    """
    SprintTestCase Prueba las funcionalidades de un Sprint

    Args:
        TestCase (TestCase): Modelo Test del módulo django
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
        "backend/api/fixtures/testing/permisos.json",
        "backend/api/fixtures/testing/roles.json",
        "backend/api/fixtures/testing/proyectos.json",
        "backend/api/fixtures/testing/permisosProyecto.json",
        "backend/api/fixtures/testing/plantillas.json",
        "backend/api/fixtures/testing/rolesProyecto.json",
        "backend/api/fixtures/testing/miembros.json",
        "backend/api/fixtures/testing/horarios.json",
        "backend/api/fixtures/testing/user-stories.json",
        "backend/api/fixtures/testing/product-backlogs.json",
        "backend/api/fixtures/testing/registro-user-stories.json",
        "backend/api/fixtures/testing/sprints.json",
        "backend/api/fixtures/testing/sprintbacklogs.json",
        "backend/api/fixtures/testing/miembrosprints.json"
    ]

    def setUp(self):
        """
        setUp Configura el TestCase
        """
        self.client = Client()

    def test_desactivar_usuario_en_sprint_activo(self):
        """
        test_desactivar_usuario_en_sprint_activo Prueba desactivar un Usuario que pertenece a un Sprint activo
        """
        print("\nProbando desactivar un usuario que pertenece a un Sprint Activo")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/usuarios/2/desactivar/")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_obtener_sprint(self):
        """
        test_obtener_sprint Prueba obtener los detalles de un Sprint
        """
        print("\nProbando obtener los detalles de un Sprint")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/sprints/1/")
        self.assertEquals(response.status_code, 200)
        sprint = Sprint.objects.get(pk=1)
        sprint_serializer = SprintSerializer(sprint, many=False)
        body = response.json()
        self.assertDictEqual(body, sprint_serializer.data)

    def test_obtener_sprint_sin_permiso_ver_sprints(self):
        """
        test_obtener_sprint_sin_permiso_ver_sprints
        Prueba obtener los detalles de un Sprint sin tener el permiso de proyecto: Ver Sprints
        """
        print("\nProbando obtener los detalles de un Sprint sin tener el permiso de proyecto: Ver Sprints")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_sprints").delete()
        response = self.client.get("/api/sprints/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_sprints"])
        self.assertEquals(body["error"], "forbidden")

    def test_obtener_sprint_no_existente(self):
        """
        test_obtener_sprint_no_existente Prueba obtener los detalles de un Sprint que no existe
        """
        print("\nProbando obtener los detalles de un Sprint que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/sprints/1000/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_obtener_sprint_sin_ser_miembro(self):
        """
        test_obtener_sprint_sin_ser_miembro Prueba obtener los detalles de un Sprint sin ser miembro del Proyecto
        """
        print("\nProbando obtener los detalles de un Sprint sin ser miembro del Proyecto")
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.get(pk=1)
        miembro.usuario_id = 2
        miembro.save()
        response = self.client.get("/api/sprints/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")
