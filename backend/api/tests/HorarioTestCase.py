from django.test import TestCase
from django.test import Client
from backend.api.models import PermisoProyecto, Horario


class HorarioTestCase(TestCase):
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

    def test_modificar_horario(self):
        """
        test_modificar_horario Prueba modificar un horario
        """
        print("\nProbando modificar un horario")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 1,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        body.pop("id")
        self.assertEquals(body, horario_body)

    def test_hora_mayor_a_24_lunes(self):
        """
        test_hora_mayor_a_24_lunes Prueba modificar un horario pasando una hora superior a 24
        """
        print("\nProbando modificar un horario con una hora superior a 24 - lunes")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 300,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["lunes"]), 1)

    def test_hora_mayor_a_24_martes(self):
        """
        test_hora_mayor_a_24_martes Prueba modificar un horario pasando una hora superior a 24
        """
        print("\nProbando modificar un horario con una hora superior a 24 - martes")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 0,
            "martes": 200,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["martes"]), 1)

    def test_hora_mayor_a_24_miercoles(self):
        """
        test_hora_mayor_a_24_miercoles Prueba modificar un horario pasando una hora superior a 24
        """
        print("\nProbando modificar un horario con una hora superior a 24 - miercoles")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 50,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["miercoles"]), 1)

    def test_hora_mayor_a_24_jueves(self):
        """
        test_hora_mayor_a_24_jueves Prueba modificar un horario pasando una hora superior a 24
        """
        print("\nProbando modificar un horario con una hora superior a 24 - jueves")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 5,
            "jueves": 9000,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["jueves"]), 1)

    def test_hora_mayor_a_24_viernes(self):
        """
        test_hora_mayor_a_24_viernes Prueba modificar un horario pasando una hora superior a 24
        """
        print("\nProbando modificar un horario con una hora superior a 24 - viernes")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 666,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["viernes"]), 1)

    def test_hora_mayor_a_24_sabado(self):
        """
        test_hora_mayor_a_24_sabado Prueba modificar un horario pasando una hora superior a 24
        """
        print("\nProbando modificar un horario con una hora superior a 24 - sabado")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": 777,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["sabado"]), 1)

    def test_hora_mayor_a_24_domingo(self):
        """
        test_hora_mayor_a_24_domingo Prueba modificar un horario pasando una hora superior a 24
        """
        print("\nProbando modificar un horario con una hora superior a 24 - domingo")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4000
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["domingo"]), 1)

    def test_hora_negativa_lunes(self):
        """
        test_hora_negativa_lunes Prueba modificar un horario pasando una hora negativa
        """
        print("\nProbando modificar un horario con una hora negativa - lunes")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": -300,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["lunes"]), 1)

    def test_hora_negativa_martes(self):
        """
        test_hora_negativa_martes Prueba modificar un horario pasando una hora negativa
        """
        print("\nProbando modificar un horario con una hora negativa - martes")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 0,
            "martes": -200,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["martes"]), 1)

    def test_hora_negativa_miercoles(self):
        """
        test_hora_negativa_miercoles Prueba modificar un horario pasando una hora negativa
        """
        print("\nProbando modificar un horario con una hora negativa - miercoles")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": -50,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["miercoles"]), 1)

    def test_hora_negativa_jueves(self):
        """
        test_hora_negativa_jueves Prueba modificar un horario pasando una hora negativa
        """
        print("\nProbando modificar un horario con una hora negativa - jueves")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 5,
            "jueves": -9000,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["jueves"]), 1)

    def test_hora_negativa_viernes(self):
        """
        test_hora_negativa_viernes Prueba modificar un horario pasando una hora negativa
        """
        print("\nProbando modificar un horario con una hora negativa - viernes")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": -666,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["viernes"]), 1)

    def test_hora_negativa_sabado(self):
        """
        test_hora_negativa_sabado Prueba modificar un horario pasando una hora negativa
        """
        print("\nProbando modificar un horario con una hora negativa - sabado")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": -777,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["sabado"]), 1)

    def test_hora_negativa_domingo(self):
        """
        test_hora_negativa_domingo Prueba modificar un horario pasando una hora negativa
        """
        print("\nProbando modificar un horario con una hora negativa - domingo")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": -4000
        }
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["domingo"]), 1)

    def test_modificar_horario_no_existente(self):
        """
        test_modificar_horario_no_existente Prueba modificar un horario que no existe
        """
        print("\nProbando modificar un horario que no existe")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        response = self.client.put("/api/horarios/1000/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_modificar_horario_sin_permiso_modificar_miembros(self):
        """
        test_modificar_horario_sin_permiso_modificar_miembros
        Prueba modificar un horario sin tener permiso para modificar miembros
        """
        print("\nProbando modificar un horario sin tener permiso para modificar miembros")
        self.client.login(username="testing", password="polijira2021")
        horario_body = {
            "lunes": 3,
            "martes": 0,
            "miercoles": 5,
            "jueves": 0,
            "viernes": 6,
            "sabado": 0,
            "domingo": 4
        }
        PermisoProyecto.objects.get(codigo="modificar_miembros").delete()
        response = self.client.put("/api/horarios/1/", horario_body, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_por_semana_method(self):
        """
        test_por_semana_method Prueba la funcionalidad del método por_semana de Horario
        """
        print("\nProbando metodo por_semana de Horario")
        horario = Horario.objects.get(pk=1)
        self.assertEquals(horario.por_semana(), 11)
