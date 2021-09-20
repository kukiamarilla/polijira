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

    def test_crear_miembro(self):
        """
        test_crear_miembro Prueba crear un miembro
        """
        print("\nProbando crear un miembro")
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
        miembro = Miembro.objects.filter(usuario=usuario, proyecto=proyecto, rol=rol)
        self.assertEquals(len(miembro), 1)
        miembro = miembro[0]
        horario = miembro.horario
        self.assertIsNotNone(horario)
        self.assertEquals(horario.lunes, request_data["horario"]["lunes"])
        self.assertEquals(horario.martes, request_data["horario"]["martes"])
        self.assertEquals(horario.miercoles, request_data["horario"]["miercoles"])
        self.assertEquals(horario.jueves, request_data["horario"]["jueves"])
        self.assertEquals(horario.viernes, request_data["horario"]["viernes"])
        self.assertEquals(horario.sabado, request_data["horario"]["sabado"])
        self.assertEquals(horario.domingo, request_data["horario"]["domingo"])

    def test_crear_miembro_rol_distinto(self):
        """
        test_crear_miembro_rol_distinto Prueba crear un miembro con un rol que no pertenece al proyecto
        """
        print("\nProbando crear un miembro con un rol que no pertenece al proyecto")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 2,
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
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_crear_miembro_usuario_no_existente(self):
        """
        test_crear_miembro_usuario_no_existente Prueba crear un miembro con un usuario que no existe
        """
        print("\nProbando crear miembro con un usuario que no existe")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 1000,
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
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)

    def test_crear_miembro_proyecto_no_existente(self):
        """
        test_crear_miembro_proyecto_no_existente Prueba crear un miembro con un proyecto que no existe
        """
        print("\nProbando crear miembro con un proyecto que no existe")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 1000,
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
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)

    def test_crear_miembro_rol_no_existente(self):
        """
        test_crear_miembro_rol_no_existente Prueba crear un miembro con un rol que no existe
        """
        print("\nProbando crear miembro con un rol que no existe")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 1,
            "rol": 1000,
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
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)

    def test_hora_mayor_a_24_lunes(self):
        """
        test_hora_mayor_a_24_lunes Prueba crear miembro con un horario pasando una hora superior a 24
        """
        print("\nProbando crear miembro con un horario con una hora superior a 24 - lunes")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 1,
            "horario": {
                "lunes": 200,
                "martes": 0,
                "miercoles": 5,
                "jueves": 0,
                "viernes": 6,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_mayor_a_24_martes(self):
        """
        test_hora_mayor_a_24_martes Prueba crear miembro con un horario pasando una hora superior a 24
        """
        print("\nProbando crear miembro con un horario con una hora superior a 24 - martes")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": 1000,
                "miercoles": 5,
                "jueves": 0,
                "viernes": 6,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_mayor_a_24_miercoles(self):
        """
        test_hora_mayor_a_24_miercoles Prueba crear miembro con un horario pasando una hora superior a 24
        """
        print("\nProbando crear miembro con un horario con una hora superior a 24 - miercoles")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": 0,
                "miercoles": 50,
                "jueves": 0,
                "viernes": 6,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_mayor_a_24_jueves(self):
        """
        test_hora_mayor_a_24_jueves Prueba crear miembro con un horario pasando una hora superior a 24
        """
        print("\nProbando crear miembro con un horario con una hora superior a 24 - jueves")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": 0,
                "miercoles": 5,
                "jueves": 2000,
                "viernes": 6,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_mayor_a_24_viernes(self):
        """
        test_hora_mayor_a_24_viernes Prueba crear miembro con un horario pasando una hora superior a 24
        """
        print("\nProbando crear miembro con un horario con una hora superior a 24 - viernes")
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
                "viernes": 60,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_mayor_a_24_sabado(self):
        """
        test_hora_mayor_a_24_sabado Prueba crear miembro con un horario pasando una hora superior a 24
        """
        print("\nProbando crear miembro con un horario con una hora superior a 24 - sabado")
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
                "sabado": 200,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_mayor_a_24_domingo(self):
        """
        test_hora_mayor_a_24_domingo Prueba crear miembro con un horario pasando una hora superior a 24
        """
        print("\nProbando crear miembro con un horario con una hora superior a 24 - domingo")
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
                "domingo": 40
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_negativa_lunes(self):
        """
        test_hora_negativa_lunes Prueba crear miembro con un horario pasando una hora negativa
        """
        print("\nProbando crear miembro con un horario con una hora negativa - lunes")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 1,
            "horario": {
                "lunes": -1,
                "martes": 0,
                "miercoles": 5,
                "jueves": 0,
                "viernes": 6,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_negativa_martes(self):
        """
        test_hora_negativa_martes Prueba crear miembro con un horario pasando una hora negativa
        """
        print("\nProbando crear miembro con un horario con una hora negativa - martes")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": -6,
                "miercoles": 5,
                "jueves": 0,
                "viernes": 6,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_negativa_miercoles(self):
        """
        test_hora_negativa_miercoles Prueba crear miembro con un horario pasando una hora negativa
        """
        print("\nProbando crear miembro con un horario con una hora negativa - miercoles")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": 0,
                "miercoles": -5,
                "jueves": 0,
                "viernes": 6,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_negativa_jueves(self):
        """
        test_hora_negativa_jueves Prueba crear miembro con un horario pasando una hora negativa
        """
        print("\nProbando crear miembro con un horario con una hora negativa - jueves")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 2,
            "rol": 2,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": 0,
                "miercoles": 5,
                "jueves": -7,
                "viernes": 6,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_negativa_viernes(self):
        """
        test_hora_negativa_viernes Prueba crear miembro con un horario pasando una hora negativa
        """
        print("\nProbando crear miembro con un horario con una hora negativa - viernes")
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
                "viernes": -6,
                "sabado": 2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_negativa_sabado(self):
        """
        test_hora_negativa_sabado Prueba crear miembro con un horario pasando una hora negativa
        """
        print("\nProbando crear miembro con un horario con una hora negativa - sabado")
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
                "sabado": -2,
                "domingo": 4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

    def test_hora_negativa_domingo(self):
        """
        test_hora_negativa_domingo Prueba crear miembro con un horario pasando una hora negativa
        """
        print("\nProbando crear miembro con un horario con una hora negativa - domingo")
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
                "domingo": -4
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horario"]), 1)

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

    def test_modificar_miembro(self):
        """
        test_modificar_miembro Prueba modificar un miembro
        """
        print("\nProbando modificar un miembro")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 2
        }
        response = self.client.put("/api/miembros/1/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        miembro = Miembro.objects.get(pk=1)
        self.assertEquals(miembro.rol.id, body["rol"]["id"], 2)

    def test_modificar_miembro_rol_no_existente(self):
        """
        test_modificar_miembro_rol_no_existente Prueba modificar un miembro pasando un rol que no existe
        """
        print("\nProbando modificar un miembro con un rol que no existe")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 2000
        }
        response = self.client.put("/api/miembros/1/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["rol"]), 1)

    def test_modificar_miembro_no_existente(self):
        """
        test_modificar_miembro_no_existente Prueba modificar un miembro que no existe
        """
        print("\nProbando modificar un miembro que no existe")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 2
        }
        response = self.client.put("/api/miembros/1000/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_eliminar_miembro(self):
        """
        test_eliminar_miembro Prueba eliminar un miembro
        """
        print("\nProbando eliminar un miembro")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/miembros/1/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(body["message"], "Miembro Eliminado")

    def test_eliminar_miembro_no_existente(self):
        """
        test_eliminar_miembro Prueba eliminar un miembro que no existe
        """
        print("\nProbando eliminar un miembro que no existe")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/miembros/1000/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_obtener_miembro(self):
        """
        test_obtener_miembro Prueba obtener un miembro
        """
        print("\nProbando obtener un miembro")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/1/")
        self.assertEquals(response.status_code, 200)
        miembro = Miembro.objects.get(pk=1)
        body = response.json()
        self.assertEquals(body["id"], miembro.id)
        self.assertEquals(body["usuario"]["id"], miembro.usuario.id)
        self.assertEquals(body["proyecto"]["id"], miembro.proyecto.id)
        self.assertEquals(body["rol"]["id"], miembro.rol.id)

    def test_obtener_miembro_no_existente(self):
        """
        test_obtener_miembro Prueba obtener un miembro que no existe
        """
        print("\nProbando obtener un miembro que no existe")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/1000/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")
