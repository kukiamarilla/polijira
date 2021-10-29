from django.test import TestCase
from django.test.client import Client
from backend.api.models import Actividad, MiembroSprint, SprintBacklog, Sprint


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
        "backend/api/fixtures/testing/miembrosprints.json",
        "backend/api/fixtures/testing/actividades.json"
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
        sprint = Sprint.objects.get(pk=2)
        sprint.estado = "A"
        sprint.save()
        request_data = {
            "sprint_backlog": 1,
            "descripcion": "Holiii",
            "horas": 2
        }
        response = self.client.post("/api/actividades/", request_data)
        body = response.json()
        actividad = Actividad.objects.filter(**body)
        self.assertEquals(len(actividad), 1)

    def test_modificar_actividad(self):
        """
        test_modificar_actividad Prueba modificar una Actividad
        """
        print("\nProbando modificar una Actividad")
        self.client.login(
            username="testing",
            password="polijira2021"
        )
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint = Sprint.objects.get(pk=2)
        sprint.estado = "A"
        sprint.save()
        request_data = {
            "descripcion": "Holiii :)",
            "horas": 3
        }
        response = self.client.put("/api/actividades/1/", request_data, content_type="application/json")
        body = response.json()
        actividad = Actividad.objects.filter(**body)
        self.assertEquals(len(actividad), 1)

    def test_eliminar_actividad(self):
        """
        test_eliminar_actividad Prueba eliminar una Actividad
        """
        print("\nProbando eliminar una Actividad")
        self.client.login(
            username="testing",
            password="polijira2021"
        )
        response = self.client.delete("/api/actividades/1/")
        self.assertEquals(response.status_code, 200)
        actividad = Actividad.objects.filter(pk=1)
        self.assertEquals(len(actividad), 0)
