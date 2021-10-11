from django.test import TestCase, Client
from backend.api.models import PermisoProyecto, Sprint, Miembro


class SprintPlanningTestCase(TestCase):
    """
    SprintPlanningTestCase Prueba las funcionalidades de un Spring Planning

    Args:
        TestCase (class): Modelo Test del módulo django
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

    def test_iniciar_sprint_planning(self):
        """
        test_iniciar_sprint_planning Prueba Iniciar un Sprint Planning
        """
        print("\nProbando Iniciar un Sprint Planning")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/sprints/2/iniciar_sprint_planning/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        sprint = Sprint.objects.filter(**body)
        self.assertEquals(len(sprint), 1)
        sprint = sprint[0]
        self.assertEquals(sprint.estado_sprint_planning, "I")

    def test_iniciar_sprint_planning_no_existente(self):
        """
        test_iniciar_sprint_planning_no_existente
        Prueba Iniciar un Sprint Planning de un Sprint que no existe en la BD
        """
        print("\nProbando Iniciar un Sprint Planning de un Sprint que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/sprints/2000/iniciar_sprint_planning/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body.get("error"), "not_found")

    def test_iniciar_sprint_planning_sin_ser_miembro(self):
        """
        test_iniciar_sprint_planning_sin_ser_miembro
        Prueba Iniciar Sprint Planning sin ser miembro del Proyecto
        """
        print("\nProbando Iniciar Sprint Planning sin ser miembro del Proyecto")
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.get(pk=4)
        miembro.usuario_id = 2
        miembro.save()
        response = self.client.post("/api/sprints/2/iniciar_sprint_planning/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body.get("error"), "forbidden")

    def test_iniciar_sprint_planning_sin_permiso_ver_sprints(self):
        """
        test_iniciar_sprint_planning_sin_permiso_ver_sprints
        Prueba Iniciar un Sprint Planning sin tener el permiso de Proyecto: Ver Sprints
        """
        print("\nProbando Iniciar un Sprint Planning sin tener el permiso de Proyecto: Ver Sprints")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_sprints").delete()
        response = self.client.post("/api/sprints/2/iniciar_sprint_planning/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body.get("error"), "forbidden")

    def test_iniciar_sprint_planning_sin_permiso_iniciar_sprint_planning(self):
        """
        test_iniciar_sprint_planning_sin_permiso_iniciar_sprint_planning
        Prueba Iniciar un Sprint Planning sin tener el permiso de Proyecto: Iniciar Sprint Planning
        """
        print("\nProbando Iniciar un Sprint Planning sin tener el permiso de Proyecto: Iniciar Sprint Planning")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="iniciar_sprint_planning").delete()
        response = self.client.post("/api/sprints/2/iniciar_sprint_planning/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body.get("error"), "forbidden")
