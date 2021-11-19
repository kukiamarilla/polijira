from django.test import TestCase
from django.test.client import Client
from backend.api.models import PermisoProyecto, Miembro, MiembroSprint, Sprint


class MiembroSprintTestCase(TestCase):
    """
    MiembroSprintTestCase Tests para probar funcionalidad de Miembro Sprint

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

    def test_eliminar_miembro_sprint(self):
        """
        test_eliminar_miembro_sprint
        Prueba eliminar miembro sprint
        """
        print("\nProbando eliminar un miembro sprint.")
        self.client.login(username="testing", password="polijira2021")
        miembro_sprint = MiembroSprint.objects.get(id=4)
        sprint = miembro_sprint.sprint
        sprint.activar()
        response = self.client.delete("/api/miembros-sprint/4/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["message"], "Miembro eliminado correctamente")

    def test_eliminar_miembro_sprint_sin_permiso_modificar_miembros_sprint(self):
        """
        test_eliminar_miembro_sprint_sin_permiso_modificar_miembros_sprint
        Prueba eliminar miembro sprint sin permiso modificar miembros sprint
        """
        print("\nProbando eliminar un miembro sprint sin permiso modificar miembros sprint.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="modificar_miembros_sprint").delete()
        response = self.client.delete("/api/miembros-sprint/4/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["modificar_miembros_sprint"])
        self.assertEquals(body["error"], "forbidden")

    def test_eliminar_miembro_sprint_inexistente(self):
        """
        test_eliminar_miembro_sprint_inexistente
        Prueba eliminar miembro sprint inexistente
        """
        print("\nProbando eliminar un miembro sprint inexistente.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/miembros-sprint/99/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "Miembro del Sprint no existe")
        self.assertEquals(body["error"], "not_found")

    def test_eliminar_miembro_sprint_sin_ser_miembro(self):
        """
        test_eliminar_miembro_sprint_sin_ser_miembro
        Prueba eliminar miembro sprint sin ser miembro del proyecto
        """
        print("\nProbando eliminar un miembro sprint sin ser miembro del proyecto.")
        self.client.login(username="user_test", password="polijira2021")
        response = self.client.delete("/api/miembros-sprint/4/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "Usted no es miembro de este Proyecto")
        self.assertEquals(body["error"], "forbidden")

    def test_reemplazar_miembro_sprint(self):
        """
        test_reemplazar_miembro_sprint
        Prueba reemplazar miembro sprint
        """
        print("\nProbando reemplazar un miembro sprint.")
        self.client.login(username="testing", password="polijira2021")
        miembro_sprint = MiembroSprint.objects.get(id=4)
        sprint = miembro_sprint.sprint
        sprint.activar()
        request_data = {
            "miembro": 4
        }
        response = self.client.post("/api/miembros-sprint/4/reemplazar/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["message"], "Miembro reemplazado correctamente")

    def test_reemplazar_miembro_sprint_con_miembro_perteneciente_al_sprint(self):
        """
        test_reemplazar_miembro_sprint_con_miembro_perteneciente_al_sprint
        Prueba reemplazar miembro sprint con un miembro perteneciente al sprint
        """
        print("\nProbando reemplazar un miembro sprint con un miembro perteneciente al sprint.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "miembro": 4
        }
        miembro_sprint = MiembroSprint.objects.get(pk=4)
        sprint = miembro_sprint.sprint
        miembro_nuevo = Miembro.objects.get(pk=request_data["miembro"])
        miembro_sprint_nuevo = MiembroSprint.objects.get(
            miembro_proyecto=miembro_nuevo, sprint=Sprint.objects.get(pk=2))
        miembro_sprint_nuevo.sprint = sprint
        miembro_sprint_nuevo.save()
        response = self.client.post("/api/miembros-sprint/4/reemplazar/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertEquals(body["message"], "El miembro ya está en el sprint")
        self.assertEquals(body["error"], "bad_request")

    def test_reemplazar_miembro_sprint_sin_permiso_modificar_miembros_sprint(self):
        """
        test_reemplazar_miembro_sprint_sin_permiso_modificar_miembros_sprint
        Prueba reemplazar miembro sprint sin permiso modificar miembros sprint
        """
        print("\nProbando reemplazar un miembro sprint sin permiso modificar miembros sprint.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "miembro": 4
        }
        PermisoProyecto.objects.get(codigo="modificar_miembros_sprint").delete()
        response = self.client.post("/api/miembros-sprint/4/reemplazar/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["modificar_miembros_sprint"])
        self.assertEquals(body["error"], "forbidden")

    def test_reemplazar_miembro_sprint_inexistente(self):
        """
        test_reemplazar_miembro_sprint_inexistente
        Prueba reemplazar miembro sprint inexistente
        """
        print("\nProbando reemplazar un miembro sprint inexistente.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "miembro": 4
        }
        response = self.client.post("/api/miembros-sprint/99/reemplazar/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "Miembro del Sprint no existe")
        self.assertEquals(body["error"], "not_found")

    def test_reemplazar_miembro_sprint_con_miembro_inexistente(self):
        """
        test_reemplazar_miembro_sprint_con_miembro_inexistente
        Prueba reemplazar miembro sprint con miembro inexistente
        """
        print("\nProbando reemplazar un miembro sprint con miembro inexistente.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "miembro": 99
        }
        response = self.client.post("/api/miembros-sprint/4/reemplazar/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "Miembro nuevo no existe")
        self.assertEquals(body["error"], "not_found")
