from django.test import TestCase, Client
from backend.api.models import PermisoProyecto, SprintBacklog


class SprintBacklogTestCase(TestCase):
    """
    SprintBacklogTestCase Prueba las funcionalidades de un Sprint Backlog

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

    def test_mover_user_story(self):
        """
        test_mover_user_story
        Prueba mover un user story a otra columna del kanban
        """
        print("\nProbando mover un user story a otra columna del kanban.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlog/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["sprint"]["id"], sprint_backlog.pk)
        self.assertEquals(body["estado_kanban"], request_data["estado_kanban"])

    def test_mover_user_story_sin_permiso_ver_kanban(self):
        """
        test_mover_user_story_sin_permiso_ver_kanban
        Prueba mover un user story a otra columna del kanban sin permiso ver kanban
        """
        print("\nProbando mover un user story a otra columna del kanban sin permiso ver kanban.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_kanban").delete()
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlog/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_kanban", "ver_user_stories", "mover_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_sin_permiso_ver_user_stories(self):
        """
        test_mover_user_story_sin_permiso_ver_user_stories
        Prueba mover un user story a otra columna del kanban sin permiso ver user stories
        """
        print("\nProbando mover un user story a otra columna del kanban sin permiso ver user stories.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlog/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_kanban", "ver_user_stories", "mover_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_sin_permiso_mover_user_stories(self):
        """
        test_mover_user_story_sin_permiso_mover_user_stories
        Prueba mover un user story a otra columna del kanban sin permiso mover user stories
        """
        print("\nProbando mover un user story a otra columna del kanban sin permiso mover user stories.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="mover_user_stories").delete()
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlog/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_kanban", "ver_user_stories", "mover_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_con_estado_kanban_sin_especificar(self):
        """
        test_mover_user_story_con_estado_kanban_sin_especificar
        Prueba mover un user story a otra columna del kanban con estado kanban sin especificar
        """
        print("\nProbando mover un user story a otra columna del kanban con estado kanban sin especificar.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        request_data = {
            "estado_kanban": None
        }
        response = self.client.post("/api/sprint-backlog/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["estado_kanban"], ["No especificaste el estado del kanban"])

    def test_mover_user_story_con_estado_kanban_no_valido(self):
        """
        test_mover_user_story_con_estado_kanban_no_valido
        Prueba mover un user story a otra columna del kanban con estado kanban no válido
        """
        print("\nProbando mover un user story a otra columna del kanban con estado kanban no válido.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        request_data = {
            "estado_kanban": "Z"
        }
        response = self.client.post("/api/sprint-backlog/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["estado_kanban"], ["Estado Kanban no válido"])

    def test_mover_user_story_con_sprint_sin_activar(self):
        """
        test_mover_user_story_con_sprint_sin_activar
        Prueba mover un user story a otra columna del kanban con sprint sin activar
        """
        print("\nProbando mover un user story a otra columna del kanban con sprint sin activar.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.sprint.finalizar()
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlog/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "El kanban no se puede modificar en el estado actual del Sprint")
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_con_sprintbacklog_inexistente(self):
        """
        test_mover_user_story_con_sprintbacklog_inexistente
        Prueba mover un user story a otra columna del kanban con sprintbacklog inexistente
        """
        print("\nProbando mover un user story a otra columna del kanban con sprint backlog inexistente.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlog/99/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "SprintBacklog no existe")
        self.assertEquals(body["error"], "not_found")
