from datetime import date
from django.test import TestCase, Client
from backend.api.models import MiembroSprint, SprintBacklog, ProductBacklog, Sprint, Usuario, Miembro, Proyecto, RegistroUserStory, UserStory, PermisoProyecto


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
