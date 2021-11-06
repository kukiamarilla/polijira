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

    def test_crear_actividad(self):
        """
        test_crear_actividad Prueba crear una Actividad
        """
        print("\nProbando crear una Actividad")
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
        self.assertEquals(response.status_code, 200)
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

    def test_error_validacion_crear_actividad_campos(self):
        """
        test_error_validacion_crear_actividad_campos
        Prueba validar la existencia de los campos: Sprint Backlog, Descripcion y Horas. En Crear Actividad
        """
        print("\nProbando validar la existencia de los campos: Sprint Backlog, Descripcion y Horas. En Crear Actividad")
        self.client.login(
            username="testing",
            password="polijira2021"
        )
        sprint = Sprint.objects.get(pk=2)
        sprint.estado = "A"
        sprint.save()
        response = self.client.post("/api/actividades/")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body.get("errors").get("sprint_backlog"), ["No se pasó: Sprint Backlog"])
        self.assertEquals(body.get("errors").get("descripcion"), ["No se pasó: Descripcion"])
        self.assertEquals(body.get("errors").get("horas"), ["No se pasó: Horas"])

    def test_error_validacion_crear_actividad_sprint_backlog(self):
        """
        test_error_validacion_crear_actividad_sprint_backlog
        Prueba validar la existencia del campo Sprint Backlog en la BD
        """
        print("\nProbando validar la existencia del campo Sprint Backlog en la BD")
        self.client.login(
            username="testing",
            password="polijira2021"
        )
        sprint = Sprint.objects.get(pk=2)
        sprint.estado = "A"
        sprint.save()
        request_data = {
            "sprint_backlog": 1000,
            "descripcion": "Holiii",
            "horas": 2
        }
        response = self.client.post("/api/actividades/", request_data)
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body.get("errors").get("sprint_backlog"), [
                          "No se encontró el Sprint Backlog en la base de datos"])

    def test_error_validacion_crear_actividad_horas(self):
        """
        test_error_validacion_crear_actividad_horas
        Prueba validar que el valor de la hora sea mayor a cero
        """
        print("\nProbando validar que el valor de la hora sea mayor a cero")
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
            "horas": -2
        }
        response = self.client.post("/api/actividades/", request_data)
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body.get("errors").get("horas"), ["La hora no puede ser negativa"])
