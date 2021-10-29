from django.test import TestCase
from django.test.client import Client
from backend.api.models import MiembroSprint, SprintBacklog


class ActividadTestCase(TestCase):
    """
    ActividadTestCase Tests para probar funcionalidad de CRUD de Actividades

    Args:
        TestCase (TestCase): Tests del módulo Django
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

    def test_registrar_actividad(self):
        """
        test_registrar_actividad Prueba registrar una Actividad
        """
        print("\nProbando registrar una Actividad")
        self.client.login(
            username="testing",
            password="polijira2021"
        )
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.desarrollador = MiembroSprint.objects.get(pk=1)
        request_data = {
            "sprint_backlog": 1,
            "descripcion": "Holiii",
            "horas": 2
        }
        response = self.client.post("/api/actividades/", request_data)
        print(response.json())
