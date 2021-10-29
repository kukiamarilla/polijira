from datetime import date
from django.test import TestCase, Client
from backend.api.models import Permiso, \
    PermisoProyecto, \
    ProductBacklog,\
    Sprint,\
    Miembro,\
    SprintBacklog,\
    UserStory,\
    MiembroSprint,\
    Proyecto
from backend.api.models.RegistroUserStory import RegistroUserStory


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
        response = self.client.post("/api/sprint-planning/2/iniciar/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        sprint = Sprint.objects.filter(**body)
        self.assertEquals(len(sprint), 1)
        sprint = sprint[0]
        self.assertEquals(sprint.estado_sprint_planning, "I")
        self.assertNotEqual(sprint.planificador, None)
        self.assertEquals(sprint.planificador.id, 4)

    def test_iniciar_sprint_planning_no_existente(self):
        """
        test_iniciar_sprint_planning_no_existente
        Prueba Iniciar un Sprint Planning de un Sprint que no existe en la BD
        """
        print("\nProbando Iniciar un Sprint Planning de un Sprint que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/sprint-planning/2000/iniciar/")
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
        response = self.client.post("/api/sprint-planning/2/iniciar/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body.get("error"), "forbidden")

    def test_iniciar_sprint_planning_sin_permiso_ver_user_stories(self):
        """
        test_iniciar_sprint_planning_sin_permiso_ver_user_stories
        Prueba Iniciar un Sprint Planning sin tener el permiso de Proyecto: Ver User Stories
        """
        print("\nProbando Iniciar un Sprint Planning sin tener el permiso de Proyecto: Ver User Stories")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        response = self.client.post("/api/sprint-planning/2/iniciar/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body.get("error"), "forbidden")

    def test_iniciar_sprint_planning_sin_permiso_ver_proyectos(self):
        """
        test_iniciar_sprint_planning_sin_permiso_ver_proyectos
        Prueba Iniciar un Sprint Planning sin tener el permiso de Sistema: Ver Proyectos
        """
        print("\nProbando Iniciar un Sprint Planning sin tener el permiso de Sistema: Ver Proyectos")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(codigo="ver_proyectos").delete()
        response = self.client.post("/api/sprint-planning/2/iniciar/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body.get("error"), "forbidden")

    def test_iniciar_sprint_planning_sin_permiso_ver_miembros(self):
        """
        test_iniciar_sprint_planning_sin_permiso_ver_miembros
        Prueba Iniciar un Sprint Planning sin tener el permiso de Proyecto: Ver Miembros
        """
        print("\nProbando Iniciar un Sprint Planning sin tener el permiso de Proyecto: Ver Miembros")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_miembros").delete()
        response = self.client.post("/api/sprint-planning/2/iniciar/")
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
        response = self.client.post("/api/sprint-planning/2/iniciar/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body.get("error"), "forbidden")

    def test_iniciar_sprint_planning_sin_permiso_planear_sprint(self):
        """
        test_iniciar_sprint_planning_sin_permiso_planear_sprint_planning
        Prueba Iniciar un Sprint Planning sin tener el permiso de Proyecto: Planear Sprint
        """
        print("\nProbando Iniciar un Sprint Planning sin tener el permiso de Proyecto: Planear Sprint")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="planear_sprints").delete()
        response = self.client.post("/api/sprint-planning/2/iniciar/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body.get("error"), "forbidden")

    def test_iniciar_sprint_planning_a_sprint_activo(self):
        """
        test_iniciar_sprint_planning_a_sprint_activo
        Prueba Iniciar un Sprint Planning a un Sprint Activo
        """
        print("\nProbando Iniciar un Sprint Planning a un Sprint Activo")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/sprint-planning/1/iniciar/")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body.get("error"), "conflict")

    def test_iniciar_sprint_planning_a_sprint_planning_no_pendiente(self):
        """
        test_iniciar_sprint_planning_a_sprint_planning_no_pendiente
        Prueba Iniciar un Sprint Planning que no tiene estado Pendiente
        """
        print("\nProbando Iniciar un Sprint Planning que no tiene estado Pendiente")
        self.client.login(username="testing", password="polijira2021")
        sprint = Sprint.objects.get(pk=2)
        sprint.estado_sprint_planning = "I"
        sprint.save()
        response = self.client.post("/api/sprint-planning/2/iniciar/")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body.get("error"), "conflict")

    def test_agregar_miembro_sprint(self):
        """
        test_agregar_miembro_sprint Prueba agregar miembro a un sprint
        """
        print("\nProbando agregar miembro a un sprint.")
        request_data = {
            "miembro": 4
        }
        sprint = Sprint.objects.get(pk=2)
        miembro = Miembro.objects.get(pk=4)
        MiembroSprint.objects.get(miembro_proyecto=miembro, sprint=sprint).delete()
        sprint.iniciar_sprint_planning(miembro)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/sprint-planning/" + str(sprint.id) + "/miembros/",
                                    request_data)
        body = response.json()
        self.assertEquals(response.status_code, 200)
        miembro = Miembro.objects.get(pk=request_data["miembro"])
        miembro_sprint = MiembroSprint.objects.filter(miembro_proyecto=miembro, sprint=sprint)
        self.assertEquals(len(miembro_sprint), 1)
        self.assertEquals(body["id"], miembro_sprint[0].id)
        self.assertEquals(body["miembro_proyecto"], miembro_sprint[0].miembro_proyecto.id)
        self.assertEquals(body["sprint"], miembro_sprint[0].sprint.id)

    def test_agregar_miembro_sprint_sin_iniciar(self):
        """
        test_agregar_miembro_sprint_sin_iniciar Prueba agregar miembro al sprint sin iniciar planificación
        """
        print("\nProbando agregar miembro al sprint sin iniciar planificación.")
        request_data = {
            "miembro": 4
        }
        sprint = Sprint.objects.get(pk=2)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/sprint-planning/" + str(sprint.id) + "/miembros/",
                                    request_data)
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "Planificación del sprint no fue iniciada")
        self.assertEquals(body["error"], "forbidden")

    def test_agregar_miembro_sprint_sin_ser_planificador(self):
        """
        test_agregar_miembro_sprint_sin_ser_planificador Prueba agregar miembro al sprint sin ser planificador
        """
        print("\nProbando agregar miembro al sprint sin ser planificador.")
        request_data = {
            "miembro": 4
        }
        sprint = Sprint.objects.get(pk=2)
        miembro = Miembro.objects.get(pk=5)
        sprint.iniciar_sprint_planning(miembro)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/sprint-planning/" + str(sprint.id) + "/miembros/",
                                    request_data)
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "Usted no es el planificador de sprint")
        self.assertEquals(body["error"], "forbidden")

    def test_agregar_miembro_sprint_miembro_no_pertenece_al_proyecto(self):
        """
        test_agregar_miembro_sprint_miembro_no_pertenece_al_proyecto
        Prueba agregar miembro al sprint con miembro no perteneciente al proyecto
        """
        print("\nProbando agregar miembro al sprint con miembro no perteneciente al proyecto.")
        request_data = {
            "miembro": 1
        }
        sprint = Sprint.objects.get(pk=2)
        miembro = Miembro.objects.get(pk=4)
        sprint.iniciar_sprint_planning(miembro)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/sprint-planning/" + str(sprint.id) + "/miembros/",
                                    request_data)
        body = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertEquals(body["message"], "El miembro no pertenece a este proyecto")
        self.assertEquals(body["error"], "bad_request")

    def test_agregar_miembro_sprint_con_sprintbacklog(self):
        """
        test_agregar_miembro_sprint_con_sprintbacklog Prueba agregar miembro al sprint con sprintbacklog
        """
        print("\nProbando agregar miembro al sprint con sprintbacklog.")
        request_data = {
            "miembro": 5
        }
        sprint = Sprint.objects.get(pk=2)

        miembro = Miembro.objects.get(pk=4)
        sprint.iniciar_sprint_planning(miembro)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/sprint-planning/" + str(sprint.id) + "/miembros/",
                                    request_data)
        body = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertEquals(body["message"], "Este paso ya se completó")
        self.assertEquals(body["error"], "bad_request")

    def test_eliminar_miembro_sprint(self):
        """
        test_eliminar_miembro_sprint Prueba eliminar un miembro de un sprint
        """
        print("\nProbando eliminar un miembro de un sprint.")
        self.client.login(username="testing", password="polijira2021")
        SprintBacklog.objects.get(pk=1).delete()
        request_data = {
            "miembro_sprint": 1
        }
        sprint = Sprint.objects.get(pk=1)
        miembro = Miembro.objects.get(pk=4)
        sprint.iniciar_sprint_planning(miembro)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/sprint-planning/" + str(sprint.id) + "/miembros/",
                                      request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        miembro_sprint = MiembroSprint.objects.filter(pk=request_data["miembro_sprint"])
        self.assertEquals(len(miembro_sprint), 0)
        self.assertEquals(body["message"], "Miembro Sprint eliminado.")

    def test_planificar_us(self):
        """
        test_planificar_us Prueba Planificar un User Story
        """
        print("\nProbando Planificar un User Story")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "user_story": 2,
            "horas_estimadas": 5,
            "desarrollador": 5
        }
        sprint = Sprint.objects.get(pk=2)
        sprint.iniciar_sprint_planning(Miembro.objects.get(pk=4))
        response = self.client.post("/api/sprint-planning/2/planificar_user_story/", request_data)
        self.assertEquals(response.status_code, 200)
        sprint_backlog = SprintBacklog.objects.filter(
            sprint_id=2,
            user_story_id=2,
            horas_estimadas=5,
            desarrollador_id=4
        )
        self.assertEquals(len(sprint_backlog), 1)

    def test_planificar_us_sprint_no_existente(self):
        """
        test_planificar_us_sprint_no_existente
        Prueba Planificar User Story con un Sprint que no existe
        """
        print("\nProbando Planificar User Story con un Sprint que no existe")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "user_story": 2,
            "horas_estimadas": 5,
            "desarrollador": 5
        }
        sprint = Sprint.objects.get(pk=2)
        sprint.iniciar_sprint_planning(Miembro.objects.get(pk=4))
        response = self.client.post("/api/sprint-planning/2000/planificar_user_story/",
                                    request_data, content_type="application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body.get("error"), "not_found")

    def test_planificar_us_no_siendo_miembro(self):
        """
        test_planificar_us_no_siendo_miembro
        Prueba Planificar User Story no siendo del Proyecto
        """
        print("\nProbando Planificar User Story no siendo del Proyecto")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "user_story": 2,
            "horas_estimadas": 5,
            "desarrollador": 5
        }
        sprint = Sprint.objects.get(pk=2)
        sprint.iniciar_sprint_planning(Miembro.objects.get(pk=4))
        miembro = Miembro.objects.get(pk=4)
        miembro.usuario_id = 2
        miembro.save()
        response = self.client.post("/api/sprint-planning/2/planificar_user_story/", request_data)
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body.get("error"), "forbidden")

    def test_planificar_us_sprint_planning_no_iniciado(self):
        """
        test_planificar_us_sprint_planning_no_iniciado
        Prueba Planificar un User Story de un Sprint Planning no Iniciado
        """
        print("\nProbando Planificar un User Story de un Sprint Planning no Iniciado")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "user_story": 2,
            "horas_estimadas": 5,
            "desarrollador": 5
        }
        response = self.client.post("/api/sprint-planning/2/planificar_user_story/",
                                    request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body.get("error"), "conflict")

    def test_planificar_us_no_siendo_planificador(self):
        """
        test_planificar_us_no_siendo_planificador
        Prueba Planificar un User Story sin ser Planificador del Sprint Planning
        """
        print("\nProbando Planificar un User Story sin ser Planificador del Sprint Planning")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "user_story": 2,
            "horas_estimadas": 5,
            "desarrollador": 5
        }
        sprint = Sprint.objects.get(pk=2)
        sprint.iniciar_sprint_planning(Miembro.objects.get(pk=2))
        response = self.client.post("/api/sprint-planning/2/planificar_user_story/",
                                    request_data, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body.get("error"), "forbidden")
