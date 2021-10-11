from django.test import TestCase, Client
from backend.api.models import MiembroSprint, Miembro
from backend.api.models.Sprint import Sprint


class MiembroSprintTestCase(TestCase):
    """
    HorarioTestCase Prueba las funcionalidades de Horario

    Args:
        TestCase (class): Clase Test del modulo test de django
    """
    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
        "backend/api/fixtures/testing/permisos.json",
        "backend/api/fixtures/testing/roles.json",
        "backend/api/fixtures/testing/proyectos.json",
        "backend/api/fixtures/testing/permisosProyecto.json",
        "backend/api/fixtures/testing/plantillas.json",
        "backend/api/fixtures/testing/miembros.json",
        "backend/api/fixtures/testing/horarios.json",
        "backend/api/fixtures/testing/rolesProyecto.json",
        "backend/api/fixtures/testing/user-stories.json",
        "backend/api/fixtures/testing/product-backlogs.json",
        "backend/api/fixtures/testing/registro-user-stories.json",
        "backend/api/fixtures/testing/sprints.json",
        "backend/api/fixtures/testing/sprintbacklogs.json",
        "backend/api/fixtures/testing/miembrosprints.json"
    ]

    def setUp(self):
        """
        setUp Configura el testcase
        """
        self.client = Client()

    def test_agregar_miembro_sprint(self):
        """
        test_agregar_miembro_sprint Prueba la agregación de miembro sprint
        """
        print("\nProbando agregar miembro sprint.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "miembro": 5
        }
        response = self.client.post("/api/miembros-sprint/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        miembro = Miembro.objects.get(pk=request_data["miembro"])
        sprint = Sprint.objects.get(pk=request_data["sprint"])
        miembro = MiembroSprint.objects.filter(miembro_proyecto=miembro, sprint=sprint)
        self.assertEquals(len(miembro), 1)
        self.assertEquals(body["id"], miembro[0].id)
        self.assertEquals(body["miembro_proyecto"], miembro[0].miembro_proyecto.id)
        self.assertEquals(body["sprint"], miembro[0].sprint.id)

    def test_eliminar_miembro_sprint(self):
        """
        test_eliminar_miembro_sprint Prueba la eliminación de miembro sprint
        """
        print("\nProbando eliminar un miembro sprint.")
        self.client.login(username="testing", password="polijira2021")
        miembro = MiembroSprint.objects.create(
            miembro_proyecto=Miembro.objects.get(pk=5),
            sprint=Sprint.objects.get(pk=1)
        )
        response = self.client.delete("/api/miembros-sprint/" + str(miembro.id) + "/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["message"], "Miembro Sprint eliminado.")

    ##################################################
    # def test_obtener_miembro_sprint(self):
    #     """
    #     test_obtener_miembro_sprint Prueba obtener miembro sprint
    #     """
    #     print("\nProbando obtener miembro sprint.")
    #     self.client.login(username="testing", password="polijira2021")
    #     response = self.client.get("/api/miembros-sprint/2/")
    #     body = response.json()
    #     self.assertEquals(response.status_code, 200)
    #     miembro = MiembroSprint.objects.get(pk=2)
    #     self.assertEquals(body["id"], miembro.id)
    #     self.assertEquals(body["miembro_proyecto"], miembro.miembro_proyecto.id)
    #     self.assertEquals(body["sprint"], miembro.sprint.id)

    # def test_obtener_miembro_sprint_inexistente(self):
    #     """
    #     test_obtener_miembro_sprint_inexistente Prueba obtener miembro sprint inexistente
    #     """
    #     print("\nProbando obtener miembro sprint inexistente.")
    #     self.client.login(username="testing", password="polijira2021")
    #     response = self.client.get("/api/miembros-sprint/99/")
    #     body = response.json()
    #     self.assertEquals(response.status_code, 404)
    #     self.assertEquals(body["message"], "No existe el Miembro en el Sprint especificado")
    #     self.assertEquals(body["error"], "not_found")

    # def test_obtener_miembro_sprint_sin_ser_miembro_proyecto(self):
    #     """
    #     test_obtener_miembro_sprint_sin_ser_miembro_proyecto
    #     Prueba obtener un miembro sprint sin ser miembro del proyecto del miembro especificado
    #     """
    #     print("\nProbando obtener un miembro sprint sin ser miembro del proyecto del miembro especificado.")
    #     self.client.login(username="testing", password="polijira2021")
    #     response = self.client.get("/api/miembros-sprint/3/")
    #     body = response.json()
    #     self.assertEquals(response.status_code, 403)
    #     self.assertEquals(body["message"], "Usted no es miembro de este proyecto")

    # def test_obtener_miembro_sprint_sin_permiso(self):
    #     """
    #     test_obtener_miembro_sprint_sin_permiso Prueba obtener miembro sprint sin permiso
    #     """
    #     print("\nProbando obtener miembro sprint sin permiso.")
    #     self.client.login(username="testing", password="polijira2021")
    #     rol = Miembro.objects.get(pk=1).rol
    #     permiso = rol.permisos.get(codigo="ver_sprints")
    #     rol.eliminar_permiso(permiso)
    #     response = self.client.get("/api/miembros-sprint/2/")
    #     body = response.json()
    #     self.assertEquals(response.status_code, 403)
    #     self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
    #     self.assertEquals(body["permission_required"], ["ver_sprints"])
    #     self.assertEquals(body["error"], "forbidden")
