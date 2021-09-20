from backend.api.models.Proyecto import Proyecto
from backend.api.models.Usuario import Usuario
from django.test import TestCase
from django.test import Client
from backend.api.models import Miembro, RolProyecto, PermisoProyecto


class MiembroTestCase(TestCase):
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
        "backend/api/fixtures/testing/rolesProyecto.json"
    ]

    def setUp(self):
        """
        setUp Configura el testcase
        """
        self.client = Client()

    def test_asignar_horario_a_miembro(self):
        """
        test_asignar_horario_a_miembro Prueba asignar un horario a un miembro
        """
        print("\nProbando asignar un horario a un miembro")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": 0,
                "miercoles": 5,
                "jueves": 0,
                "viernes": 6,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        usuario = Usuario.objects.get(pk=2)
        proyecto = Proyecto.objects.get(pk=1)
        rol = RolProyecto.objects.get(pk=2)
        miembro = Miembro.objects.get(usuario=usuario, proyecto=proyecto, rol=rol)
        self.assertIsNotNone(miembro.horario)
        horario = miembro.horario
        self.assertEquals(horario.lunes, request_data["horario"]["lunes"])
        self.assertEquals(horario.martes, request_data["horario"]["martes"])
        self.assertEquals(horario.miercoles, request_data["horario"]["miercoles"])
        self.assertEquals(horario.jueves, request_data["horario"]["jueves"])
        self.assertEquals(horario.viernes, request_data["horario"]["viernes"])
        self.assertEquals(horario.sabado, request_data["horario"]["sabado"])
        self.assertEquals(horario.domingo, request_data["horario"]["domingo"])

    def test_obtener_horario(self):
        """
        test_obtener_horario Prueba obtener un horario de un miembro
        """
        print("\nProbando obtener un horario de un miembro")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/1/horario/", content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        horarioBD = Miembro.objects.get(pk=1).horario
        self.assertEquals(body["id"], horarioBD.id)

    def test_obtener_horario_de_miembro_no_existente(self):
        """
        test_obtener_horario_de_miembro_no_existente Prueba obtener un horario de un miembro que no existe
        """
        print("\nProbando obtener un horario de un miembro que no existe")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/1000/horario/", content_type="application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_obtener_horario_sin_permiso_ver_miembros(self):
        """
        test_obtener_horario_sin_permiso_ver_miembros Prueba obtener un horario sin permiso ver miembros
        """
        print("\nProbando obtener un horario sin tener permiso ver miembros")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_miembros").delete()
        response = self.client.get("/api/miembros/1/horario/", content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")
