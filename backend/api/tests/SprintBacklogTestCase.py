from datetime import date
from django.test import TestCase
from django.test.client import Client
from backend.api.models import Permiso, \
    PermisoProyecto, \
    ProductBacklog,\
    Sprint,\
    Miembro,\
    SprintBacklog,\
    UserStory,\
    MiembroSprint,\
    Proyecto, \
    RegistroUserStory


class SprintBacklogTestCase(TestCase):

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

    def test_responder_estimacion(self):
        """
        test_responder_estimacion Prueba responder una estimacion de un Sprint Planning
        """
        print("\nProbando responder una estimacion de un Sprint Planning")
        self.client.login(username="testing", password="polijira2021")
        sprint = Sprint.objects.get(pk=2)
        sprint.iniciar_sprint_planning(Miembro.objects.get(pk=4))
        user_story_antes = UserStory.objects.get(pk=2)
        desarrollador = MiembroSprint.objects.get(pk=2)
        sprint.planificar(
            user_story=user_story_antes,
            horas_estimadas=2,
            desarrollador=desarrollador,
            planificador=Miembro.objects.get(pk=4),
            product_backlog_handler=ProductBacklog.eliminar_user_story,
            sprint_backlog_handler=SprintBacklog.agregar_user_story,
            registro_handler=RegistroUserStory.modificar_registro
        )
        request_data = {
            "horas_estimadas": 5
        }
        response = self.client.post("/api/sprint-planning/2/responder_estimacion/", request_data)
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(body.get("user_story").get("horas_estimadas"), int((2 + 5)/2))
        self.assertEquals(body.get("user_story").get("estado_estimacion"), "C")
        registro = RegistroUserStory.objects.filter(
            nombre_antes=user_story_antes.nombre,
            descripcion_antes=user_story_antes.descripcion,
            horas_estimadas_antes=2,
            prioridad_antes=user_story_antes.prioridad,
            estado_antes=user_story_antes.estado,
            desarrollador_antes=desarrollador.miembro_proyecto,
            nombre_despues=user_story_antes.nombre,
            descripcion_despues=user_story_antes.descripcion,
            horas_estimadas_despues=body.get("user_story").get("horas_estimadas"),
            prioridad_despues=user_story_antes.prioridad,
            estado_despues=user_story_antes.estado,
            desarrollador_despues=desarrollador.miembro_proyecto,
            user_story=user_story_antes,
            accion="Modificacion",
            fecha=date.today(),
            autor=4
        )
        self.assertEquals(len(registro), 1)
