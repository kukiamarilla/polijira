from django.test import TestCase
from django.test.client import Client
from backend.api.models import PermisoProyecto, \
    Sprint,\
    Miembro,\
    SprintBacklog,\
    UserStory,\
    MiembroSprint


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
        Prueba mover un user story en el kanban
        """
        print("\nProbando mover un user story en el kanban.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.sprint.activar()
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["sprint"]["id"], sprint_backlog.sprint.pk)
        self.assertEquals(body["estado_kanban"], request_data["estado_kanban"])

    def test_mover_user_story_sin_permiso_ver_kanban(self):
        """
        test_mover_user_story_sin_permiso_ver_kanban
        Prueba mover un user story en el kanban sin permiso ver kanban
        """
        print("\nProbando mover un user story en el kanban sin permiso ver kanban.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_kanban").delete()
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.sprint.activar()
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_kanban", "ver_user_stories", "mover_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_sin_permiso_ver_user_stories(self):
        """
        test_mover_user_story_sin_permiso_ver_user_stories
        Prueba mover un user story en el kanban sin permiso ver user stories
        """
        print("\nProbando mover un user story en el kanban sin permiso ver user stories.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.sprint.activar()
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_kanban", "ver_user_stories", "mover_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_sin_permiso_mover_user_stories_y_sin_ser_desarrollador(self):
        """
        test_mover_user_story_sin_permiso_mover_user_stories_y_sin_ser_desarrollador
        Prueba mover un user story en el kanban sin permiso mover user stories y sin ser desarrollador
        """
        print("\nProbando mover un user story en el kanban sin permiso mover user stories y sin ser desarrollador.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="mover_user_stories").delete()
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.desarrollador = MiembroSprint.objects.get(pk=1)
        sprint_backlog.save()
        request_data = {
            "estado_kanban": "D"
        }
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_kanban", "ver_user_stories", "mover_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_sin_permiso_mover_user_stories_y_siendo_desarrollador(self):
        """
        test_mover_user_story_sin_permiso_mover_user_stories_y_siendo_desarrollador
        Prueba mover un user story en el kanban sin permiso mover user stories y siendo desarrollador
        """
        print("\nProbando mover un user story en el kanban sin permiso mover user stories y siendo desarrollador.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="mover_user_stories").delete()
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.sprint.activar()
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["sprint"]["id"], sprint_backlog.sprint.pk)
        self.assertEquals(body["estado_kanban"], request_data["estado_kanban"])

    def test_mover_user_story_con_permiso_mover_user_stories_y_sin_ser_desarrollador(self):
        """
        test_mover_user_story_con_permiso_mover_user_stories_y_sin_ser_desarrollador
        Prueba mover un user story en el kanban con permiso mover user stories y sin ser desarrollador
        """
        print("\nProbando mover un user story en el kanban con permiso mover user stories y sin ser desarrollador.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.sprint.activar()
        user_story = sprint_backlog.user_story
        user_story.desarrollador = MiembroSprint.objects.get(pk=1)
        user_story.save()
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["sprint"]["id"], sprint_backlog.sprint.pk)
        self.assertEquals(body["estado_kanban"], request_data["estado_kanban"])

    def test_mover_user_story_con_estado_kanban_sin_especificar(self):
        """
        test_mover_user_story_con_estado_kanban_sin_especificar
        Prueba mover un user story en el kanban con estado kanban sin especificar
        """
        print("\nProbando mover un user story en el kanban con estado kanban sin especificar.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        request_data = {
            "estado_kanban": None
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["estado_kanban"], ["No especificaste el estado del kanban"])

    def test_mover_user_story_con_estado_kanban_no_valido(self):
        """
        test_mover_user_story_con_estado_kanban_no_valido
        Prueba mover un user story en el kanban con estado kanban no válido
        """
        print("\nProbando mover un user story en el kanban con estado kanban no válido.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        request_data = {
            "estado_kanban": "Z"
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["estado_kanban"], ["Estado Kanban no válido"])

    def test_mover_user_story_con_sprint_sin_activar(self):
        """
        test_mover_user_story_con_sprint_sin_activar
        Prueba mover un user story en el kanban con sprint sin activar
        """
        print("\nProbando mover un user story en el kanban con sprint sin activar.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.sprint.finalizar()
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "El kanban no se puede modificar en el estado actual del Sprint")
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_con_user_story_cancelado(self):
        """
        test_mover_user_story_con_user_story_cancelado
        Prueba mover un user story cancelado en el kanban
        """
        print("\nProbando mover un user story cancelado en el kanban.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.sprint.activar()
        user_story = sprint_backlog.user_story
        user_story.estado = "C"
        user_story.save()
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No se puede modificar el kanban de un user story lanzado o cancelado")
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_con_user_story_lanzado(self):
        """
        test_mover_user_story_con_user_story_lanzado
        Prueba mover un user story lanzado en el kanban
        """
        print("\nProbando mover un user story lanzado en el kanban.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.sprint.activar()
        user_story = sprint_backlog.user_story
        user_story.estado = "R"
        user_story.save()
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No se puede modificar el kanban de un user story lanzado o cancelado")
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_sin_ser_miembro_del_proyecto(self):
        """
        test_mover_user_story_sin_ser_miembro_del_proyecto
        Prueba mover un user story en el kanban sin ser miembro del proyecto
        """
        print("\nProbando mover un user story en el kanban sin ser miembro del proyecto.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=2)
        sprint_backlog.sprint.activar()
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "Usted no es miembro de este Proyecto")
        self.assertEquals(body["error"], "forbidden")

    def test_mover_user_story_con_sprint_backlog_inexistente(self):
        """
        test_mover_user_story_con_sprint_backlog_inexistente
        Prueba mover un user story en el kanban con sprint backlog inexistente
        """
        print("\nProbando mover un user story en el kanban con sprint backlog inexistente.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprint-backlogs/99/mover/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "SprintBacklog no existe")
        self.assertEquals(body["error"], "not_found")

    def test_responder_estimacion(self):
        """
        test_responder_estimacion Prueba responder una estimacion de un Sprint Planning
        """
        print("\nProbando responder una estimacion de un Sprint Planning")
        self.client.login(username="testing", password="polijira2021")
        sprint = Sprint.objects.get(pk=2)
        sprint.iniciar_sprint_planning(Miembro.objects.get(pk=4))
        user_story = UserStory.objects.get(pk=2)
        sprint_backlog = SprintBacklog.objects.get(sprint=sprint, user_story=user_story)
        sprint_backlog.estado_estimacion = "p"
        sprint_backlog.save()
        h1 = sprint_backlog.horas_estimadas
        request_data = {
            "horas_estimadas": 5
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.id) +
                                    "/responder_estimacion/", request_data)
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body.get("horas_estimadas"), int((h1 + request_data["horas_estimadas"])/2))
        self.assertEquals(body.get("estado_estimacion"), "C")
        self.assertEquals(body.get("desarrollador").get("id"), 2)

    def test_reasignar_sprint_backlog(self):
        """
        test_reasignar_sprint_backlog
        Prueba reasignar un user story a otro desarrollador
        """
        print("\nProbando reasignar un user story a otro desarrollador.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.desarrollador = None
        sprint_backlog.save()
        sprint_backlog.sprint.activar()
        request_data = {
            "miembro_sprint": 2
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/reasignar/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["desarrollador"]["id"], 2)

    def test_reasignar_sprint_backlog_con_sprint_backlog_inexistente(self):
        """
        test_reasignar_sprint_backlog_con_sprint_backlog_inexistente
        Prueba reasignar un user story a otro desarrollador con sprint backlog inexistente
        """
        print("\nProbando reasignar un user story a otro desarrollador con sprint backlog inexistente.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "miembro_sprint": 2
        }
        response = self.client.post("/api/sprint-backlogs/99/reasignar/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "El User Story no existe en el sprint.")
        self.assertEquals(body["error"], "not_found")

    def test_reasignar_sprint_backlog_con_miembro_sprint_inexistente(self):
        """
        test_reasignar_sprint_backlog_con_miembro_sprint_inexistente
        Prueba reasignar un user story a otro desarrollador con miembro sprint inexistente
        """
        print("\nProbando reasignar un user story a otro desarrollador con miembro sprint inexistente.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.desarrollador = None
        sprint_backlog.save()
        sprint_backlog.sprint.activar()
        request_data = {
            "miembro_sprint": 99
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/reasignar/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "El Miembro del Sprint no existe")
        self.assertEquals(body["error"], "not_found")

    def test_reasignar_sprint_backlog_con_sprint_inactivo(self):
        """
        test_reasignar_sprint_backlog_con_sprint_inactivo
        Prueba reasignar un user story a otro desarrollador con sprint inactivo
        """
        print("\nProbando reasignar un user story a otro desarrollador con sprint inactivo.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.desarrollador = None
        sprint_backlog.save()
        request_data = {
            "miembro_sprint": 2
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/reasignar/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertEquals(body["message"], "No se puede reasignar un User Story en un sprint que no está activo.")
        self.assertEquals(body["error"], "bad_request")

    def test_reasignar_sprint_backlog_ya_asignado(self):
        """
        test_reasignar_sprint_backlog_ya_asignado
        Prueba reasignar un user story a otro desarrollador con sprint backlog ya asignado
        """
        print("\nProbando reasignar un user story a otro desarrollador con sprint backlog ya asignado.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.sprint.activar()
        request_data = {
            "miembro_sprint": 2
        }
        response = self.client.post("/api/sprint-backlogs/" + str(sprint_backlog.pk) + "/reasignar/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertEquals(body["message"], "No se puede reasignar un User Story que no está pendiente de asignación.")
        self.assertEquals(body["error"], "bad_request")
