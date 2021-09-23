from backend.api.models import \
    PlantillaRolProyecto, \
    Permiso
from django.test import TestCase, Client


class PlantillaRolProyectoTestCase(TestCase):
    """
    PlantillaRolProyectoTestCase Prueba las funcionalidades de una Plantilla de Rol de Proyecto
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
        "backend/api/fixtures/testing/permisos.json",
        "backend/api/fixtures/testing/roles.json",
        "backend/api/fixtures/testing/permisosProyecto.json",
        "backend/api/fixtures/testing/plantillas.json"
    ]

    def setUp(self):
        """
        setUp Configura el testcase
        """
        self.client = Client()

        """
         Test de CRUD de Plantilla en un escenario donde se cumplen los requerimientos
        """

    def test_listar_plantillas(self):
        """
        test_listar_plantillas Prueba obtener todas las plantillas de rol de proyecto
        """
        print("\nProbando listar plantillas.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/plantillas/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(PlantillaRolProyecto.objects.count(), len(body))

    def test_obtener_plantilla(self):
        """
        test_obtener_plantilla Prueba obtener una plantilla de rol de proyecto
        """
        print("\nProbando obtener una plantilla")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/plantillas/1/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        plantilla = PlantillaRolProyecto.objects.get(pk=1)
        self.assertGreater(len(body), 0)
        self.assertEquals(body["id"], 1)
        self.assertEquals(body["nombre"], plantilla.nombre)
        self.assertEquals(len(body["permisos"]), plantilla.permisos.count())

    def test_crear_plantilla(self):
        """
        test_crear_plantilla Prueba crear una plantilla de rol de proyecto
        """
        print("\nProbando crear una plantilla")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "PlantillaTest",
            "permisos": [
                {"id": 1},
                {"id": 2}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, "application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(body["nombre"], plantilla["nombre"])
        self.assertEquals(len(body["permisos"]), 2)

    def test_modificar_plantilla(self):
        """
        test_modificar_plantilla Prueba modificar una plantilla de rol de proyecto
        """
        print("\nProbando crear una plantilla")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "PlantillaModificadoTest"
        }
        response = self.client.put("/api/plantillas/1/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(body["id"], 1)
        self.assertEquals(body["nombre"], plantilla["nombre"])

    def test_eliminar_plantilla(self):
        """
        test_eliminar_plantilla Prueba eliminar una plantilla de rol de proyecto
        """
        print("\nProbando eliminar una plantilla")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/plantillas/1/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(body["message"], "Plantilla de rol Eliminado")

    def test_listar_permisos(self):
        """
        test_listar_permisos Prueba obtener todos los permisos de una plantilla
        """
        print("\nProbando obtener todos los permisos de una plantilla")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/plantillas/1/permisos/")
        self.assertEquals(response.status_code, 200)
        plantilla = PlantillaRolProyecto.objects.get(pk=1)
        permisos = plantilla.permisos.all()
        body = response.json()
        self.assertEquals(len(body), len(permisos))

    def test_agregar_permiso(self):
        """
        test_agregar_permiso Prueba agregar un permiso a una plantilla
        """
        print("\nProbando agregar un permiso a una plantilla")
        self.client.login(username="testing", password="polijira2021")
        permiso = {"id": 2}
        response = self.client.post("/api/plantillas/1/permisos/", permiso, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        plantilla = PlantillaRolProyecto.objects.get(pk=1)
        self.assertEquals(len(body["permisos"]), plantilla.permisos.count())

    def test_eliminar_permiso(self):
        """
        test_eliminar_permiso Prueba eliminar un permiso a una plantilla
        """
        print("\nProbando eliminar un permiso de una plantilla")
        self.client.login(username="testing", password="polijira2021")
        permiso = {"id": 1}
        response = self.client.delete("/api/plantillas/1/permisos/", permiso, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        plantilla = PlantillaRolProyecto.objects.get(pk=1)
        self.assertEquals(len(body["permisos"]), plantilla.permisos.count())

        """
         Test de CRUD de Plantilla en un escenario donde no se tiene los permisos necesarios
        """

    def test_listar_plantillas_sin_permiso_ver_plantillas(self):
        """
        test_listar_plantillas_sin_permiso_ver_plantillas
        Prueba listar plantillas sin tener el permiso Ver Plantillas de Rol de Proyecto
        """
        print("\nProbando listar plantillas sin permiso para ver plantillas")
        self.client.login(username="testing", password="polijira2021")
        permiso = Permiso.objects.get(pk=14)
        permiso.delete()
        response = self.client.get("/api/plantillas/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_plantillas"])

    def test_obtener_plantilla_sin_permiso_ver_plantillas(self):
        """
        test_obtener_plantilla_sin_permiso_ver_plantillas
        Prueba obtener una plantilla sin tener el permiso Ver Plantillas de Rol de Proyecto
        """
        print("\nProbando obtener plantilla sin permiso ver plantillas")
        self.client.login(username="testing", password="polijira2021")
        permiso = Permiso.objects.get(pk=14)
        permiso.delete()
        response = self.client.get("/api/plantillas/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_plantillas", "ver_permisos"])

    def test_obtener_plantilla_sin_permiso_ver_permisos(self):
        """
        test_obtener_plantilla_sin_permiso_ver_permisos
        Prueba obtener una plantilla sin tener el permiso Ver Permisos
        """
        print("\nProbando obtener plantilla sin permiso ver permisos")
        self.client.login(username="testing", password="polijira2021")
        permiso = Permiso.objects.get(pk=4)
        permiso.delete()
        response = self.client.get("/api/plantillas/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_plantillas", "ver_permisos"])

    def test_crear_plantilla_sin_permiso_crear_plantillas(self):
        """
        test_crear_plantilla_sin_permiso_crear_plantillas
        Prueba crear una plantilla sin el permiso de sistema Crear Plantillas de Rol de Proyecto
        """
        print("\nProbando crear una plantilla sin permiso crear plantillas")
        self.client.login(username="testing", password="polijira2021")
        permiso = Permiso.objects.get(pk=15)
        permiso.delete()
        plantilla = {
            "nombre": "PlantillaTest",
            "permisos": [
                {"id": 1},
                {"id": 2}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_permisos", "crear_plantillas"])

    def test_crear_plantilla_sin_permiso_ver_permisos(self):
        """
        test_crear_plantilla_sin_permiso_ver_permisos
        Prueba crear una plantilla sin el permiso de sistema Ver Permisos
        """
        print("\nProbando crear una plantilla sin permiso ver permisos")
        self.client.login(username="testing", password="polijira2021")
        permiso = Permiso.objects.get(pk=4)
        permiso.delete()
        plantilla = {
            "nombre": "PlantillaTest",
            "permisos": [
                {"id": 1},
                {"id": 2}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_permisos", "crear_plantillas"])

    def test_modificar_plantilla_sin_permiso_ver_plantillas(self):
        """
        test_modificar_plantilla_sin_permiso_ver_plantillas
        Prueba modificar una plantilla sin el permiso de sistema Ver Plantillas de Rol de Proyecto
        """
        print("\nProbando modificar una plantilla sin permiso ver plantillas")
        self.client.login(username="testing", password="polijira2021")
        permiso = Permiso.objects.get(pk=14)
        permiso.delete()
        plantilla = {
            "nombre": "PlantillaTest"
        }
        response = self.client.put("/api/plantillas/1/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_plantillas", "modificar_plantillas"])

    def test_modificar_plantilla_sin_permiso_modificar_plantillas(self):
        """
        test_modificar_plantilla_sin_permiso_modificar_plantillas
        Prueba modificar una plantilla sin el permiso de sistema Modificar Plantillas de Rol de Proyecto
        """
        print("\nProbando modificar una plantilla sin permiso modificar plantillas")
        self.client.login(username="testing", password="polijira2021")
        permiso = Permiso.objects.get(pk=16)
        permiso.delete()
        plantilla = {
            "nombre": "PlantillaTest"
        }
        response = self.client.put("/api/plantillas/1/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_plantillas", "modificar_plantillas"])

    def test_eliminar_plantilla_sin_permiso_ver_plantillas(self):
        """
        test_eliminar_plantilla_sin_permiso_ver_plantillas
        Prueba eliminar una plantilla sin el permiso de sistema Ver Plantillas de Rol de Proyecto
        """
        print("\nProbando eliminar una plantilla sin permiso ver plantillas")
        self.client.login(username="testing", password="polijira2021")
        permiso = Permiso.objects.get(pk=14)
        permiso.delete()
        response = self.client.delete("/api/plantillas/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_plantillas", "eliminar_plantillas"])

    def test_eliminar_plantilla_sin_permiso_eliminar_plantillas(self):
        """
        test_eliminar_plantilla_sin_permiso_eliminar_plantillas
        Prueba eliminar una plantilla sin el permiso de sistema Eliminar Plantillas de Rol de Proyecto
        """
        print("\nProbando eliminar una plantilla sin permiso eliminar plantillas")
        self.client.login(username="testing", password="polijira2021")
        permiso = Permiso.objects.get(pk=17)
        permiso.delete()
        response = self.client.delete("/api/plantillas/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_plantillas", "eliminar_plantillas"])

    def test_listar_permisos_sin_permiso_ver_plantillas(self):
        """
        test_listar_permisos_sin_permiso_ver_plantillas
        Prueba listar los permisos de una plantilla sin permiso de sistema Ver Plantillas de Rol Proyecto
        """
        print("\nProbando listar los permisos de una plantilla sin permiso ver plantillas")
        self.client.login(username="testing", password="polijira2021")
        permiso = Permiso.objects.get(pk=14)
        permiso.delete()
        response = self.client.get("/api/plantillas/1/permisos/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_plantillas"])

    def test_agregar_permiso_sin_permiso_ver_permisos(self):
        """
        test_agregar_permiso_sin_permiso_ver_permisos
        Prueba agregar un permiso a una plantilla sin tener permiso de sistema Ver Permisos
        """
        print("\nProbando agregar un permiso a una plantilla sin tener permiso ver permisos")
        self.client.login(username="testing", password="polijira2021")
        _permiso = {"id": 2}
        permiso = Permiso.objects.get(pk=4)
        permiso.delete()
        response = self.client.post("/api/plantillas/1/permisos/", _permiso, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_permisos", "modificar_plantillas"])

    def test_agregar_permiso_sin_permiso_modificar_plantillas(self):
        """
        test_agregar_permiso_sin_permiso_modificar_plantillas
        Prueba agregar un permiso a una plantilla sin tener permiso de sistema Modificar Plantillas de Rol de Proyecto
        """
        print("\nProbando agregar un permiso a una plantilla sin tener permiso ver permisos")
        self.client.login(username="testing", password="polijira2021")
        _permiso = {"id": 2}
        permiso = Permiso.objects.get(pk=16)
        permiso.delete()
        response = self.client.post("/api/plantillas/1/permisos/", _permiso, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_permisos", "modificar_plantillas"])

    def test_eliminar_permiso_sin_permiso_ver_plantillas(self):
        """
        test_eliminar_permiso_sin_permiso_ver_plantillas [summary]
        """
        print("\nProbando eliminar un permiso sin tener permiso de ver plantillas")
        self.client.login(username="testing", password="polijira2021")
        _permiso = {"id": 2}
        permiso = Permiso.objects.get(pk=14)
        permiso.delete()
        response = self.client.delete("/api/plantillas/1/permisos/", _permiso, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_plantillas", "modificar_plantillas"])

    def test_eliminar_permiso_sin_permiso_modificar_plantillas(self):
        """
        test_eliminar_permiso_sin_permiso_modificar_plantillas
        Prueba eliminar un permiso a una plantilla sin tener permiso de sistema Modificar Plantillas de Rol de Proyecto
        """
        print("\nProbando eliminar un permiso a una plantilla sin tener permiso de modificar plantillas")
        self.client.login(username="testing", password="polijira2021")
        _permiso = {"id": 2}
        permiso = Permiso.objects.get(pk=16)
        permiso.delete()
        response = self.client.delete("/api/plantillas/1/permisos/", _permiso, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_plantillas", "modificar_plantillas"])

    """
         Test de CRUD de Plantilla de Rol de Proyecto en un escenario donde:
            No se puede validar los datos
            No existen en la base de datos
    """

    def test_obtener_plantilla_no_existente(self):
        """
        test_obtener_plantilla_no_existente Prueba obtener una plantilla que no existe en la base de datos
        """
        print("\nProbando obtener una plantilla que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/plantillas/1000/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_crear_plantilla_con_algun_permiso_no_existente(self):
        """
        test_crear_plantilla_con_algun_permiso_no_existente
        Prueba crear una plantilla donde algunos de los permisos recibidos no existe en la base de datos
        """
        print("\nProbando crear una plantilla con un permiso que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "PlantillaTest",
            "permisos": [
                {"id": 1000}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["permisos"]), 1)

    def test_crear_plantilla_sin_nombre(self):
        """
        test_crear_plantilla_sin_nombre Prueba crear una plantilla sin especificar el nombre
        """
        print("\nProbando crear una plantilla sin especificar el nombre")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "permisos": [
                {"id": 1}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_crear_plantilla_sin_permisos(self):
        """
        test_crear_plantilla_sin_permisos Prueba crear una plantilla sin especificar ningun permiso
        """
        print("\nProbando crear una plantilla sin especificar algun permiso")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "PlantillaTest"
        }
        response = self.client.post("/api/plantillas/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["permisos"]), 1)

    def test_crear_plantilla_con_nombre_superior_a_max_length(self):
        """
        test_crear_plantilla_con_nombre_superior_a_max_length
        Prueba crear una plantilla con un nombre superior a la maxima longitud
        """
        print("\nProbando crear una plantilla con un nombre que supere la longitud maxima")
        self.client.login(username="testing", password="polijira2021")
        nombre_max_length = ""
        for i in range(0, 256):
            nombre_max_length += "a"
        plantilla = {
            "nombre": nombre_max_length,
            "permisos": [
                {"id": 1}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_modificar_plantilla_no_existente(self):
        """
        test_modificar_plantilla_no_existente Prueba modificar una plantilla que no existe en la base de datos
        """
        print("\nProbando modificar una plantilla que no existe en la base de datos")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "PlantillaTest",
            "permisos": [
                {"id": 1}
            ]
        }
        response = self.client.put("/api/plantillas/1000/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_modificar_plantilla_sin_nombre(self):
        """
        test_modificar_plantilla_sin_nombre Prueba modificar una plantilla sin especificar un nombre
        """
        print("\nProbando modificar una plantilla sin especificar un nombre")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "permisos": [
                {"id": 1}
            ]
        }
        response = self.client.put("/api/plantillas/1/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_modificar_plantilla_con_nombre_superior_a_max_length(self):
        """
        test_modificar_plantilla_con_nombre_superior_a_max_length
        Prueba modificar una plantilla donde el nombre especificado supera la longitud máxima
        """
        print("\nProbando modificar una plantilla con un nombre que supera la longitud máxima")
        self.client.login(username="testing", password="polijira2021")
        nombre_max_length = ""
        for i in range(0, 256):
            nombre_max_length += "a"
        plantilla = {
            "nombre": nombre_max_length,
            "permisos": [
                {"id": 1}
            ]
        }
        response = self.client.put("/api/plantillas/1/", plantilla, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_eliminar_plantilla_no_existente(self):
        """
        test_eliminar_plantilla_no_existente Prueba eliminar una plantilla que no existe en la base de datos
        """
        print("\nProbando eliminar una plantilla que no existe en la base de datos")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/plantillas/1000/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_listar_permiso_a_plantilla_no_existente(self):
        """
        test_listar_permiso_a_plantilla_no_existente Prueba listar los permisos de una plantilla que no existe
        """
        print("\nProbando listar los permisos de una plantilla que no existe")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/plantillas/1000/permisos/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_agregar_permiso_no_existente(self):
        """
        test_agregar_permiso_no_existente Prueba agregar un permiso que no existe en la base de datos
        """
        print("\nProbando agregar permiso que no existe en la base de datos")
        self.client.login(username="testing", password="polijira2021")
        permiso = {"id": 1000}
        response = self.client.post("/api/plantillas/1/permisos/", permiso, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["id"]), 1)

    def test_agregar_permiso_sin_permiso(self):
        """
        test_agregar_permiso_sin_permiso Prueba agregar un permiso sin especificar ningún permiso
        """
        print("\nProbando agregar un permiso sin especificar ningun permiso a una plantilla")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/plantillas/1/permisos/")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["id"]), 1)

    def test_agregar_permiso_a_plantilla_no_existente(self):
        """
        test_agregar_permiso_a_plantilla_no_existente
        Prueba agregar un permiso a una plantilla que no existe en la base de datos
        """
        print("\nProbando agregar un permiso a una plantilla que no existe en la base de datos")
        self.client.login(username="testing", password="polijira2021")
        permiso = {"id": 2}
        response = self.client.post("/api/plantillas/1000/permisos/", permiso, content_type="application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_eliminar_permiso_no_existente(self):
        """
        test_eliminar_permiso_no_existente Prueba eliminar un permiso que no existe a una plantilla
        """
        print("\nProbando eliminar un permiso que no existe de una plantilla")
        self.client.login(username="testing", password="polijira2021")
        permiso = {"id": 1000}
        response = self.client.delete("/api/plantillas/1/permisos/", permiso, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["id"]), 1)

    def test_eliminar_permiso_a_plantilla_no_existente(self):
        """
        test_eliminar_permiso_a_plantilla_no_existente
        Prueba eliminar un permiso a una plantilla que no existe en la base de datos

        """
        print("\nProbando eliminar un permiso a una plantilla que no existe")
        self.client.login(username="testing", password="polijira2021")
        permiso = {"id": 2}
        response = self.client.delete("/api/plantillas/1000/permisos/", permiso, content_type="application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_crear_plantilla_existente_sm(self):
        """
        test_crear_plantilla_existente_sm Prueba crear una plantilla con el nombre Scrum Master
        """
        print("\nProbando crear una plantilla con el nombre de Scrum Master")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "Scrum Master",
            "permisos": [
                {"id": 1},
                {"id": 2}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_crear_plantilla_existente_tm(self):
        """
        test_crear_plantilla_existente_tm Prueba crear una plantilla con el nombre Team Member
        """
        print("\nProbando crear una plantilla con el nombre de Team Member")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "Team Member",
            "permisos": [
                {"id": 1},
                {"id": 2}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_crear_plantilla_existente_po(self):
        """
        test_crear_plantilla_existente_po Prueba crear una plantilla con el nombre Product Owner
        """
        print("\nProbando crear una plantilla con el nombre de Product Owner")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "Product Owner",
            "permisos": [
                {"id": 1},
                {"id": 2}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_crear_plantilla_existente_sh(self):
        """
        test_crear_plantilla_existente_sh Prueba crear una plantilla con el nombre Stake Holder
        """
        print("\nProbando crear una plantilla con el nombre de Stake Holder")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "Stake Holder",
            "permisos": [
                {"id": 1},
                {"id": 2}
            ]
        }
        response = self.client.post("/api/plantillas/", plantilla, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_modificar_plantilla_con_nombre_existente_sm(self):
        """
        test_modificar_plantilla_con_nombre_existente_sm
        Prueba modificar una plantilla y asignar el nombre Scrum Master
        """
        print("\nProbando modificar una plantilla y asignar el nombre de Scrum Master")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "Scrum Master"
        }
        response = self.client.put("/api/plantillas/2/", plantilla, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_modificar_plantilla_con_nombre_existente_tm(self):
        """
        test_modificar_plantilla_con_nombre_existente_tm Prueba modificar una plantilla y asignar el nombre Team Member
        """
        print("\nProbando modificar una plantilla y asignar el nombre de Team Member")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "Team Member"
        }
        response = self.client.put("/api/plantillas/1/", plantilla, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_modificar_plantilla_con_nombre_existente_po(self):
        """
        test_modificar_plantilla_con_nombre_existente_po
        Prueba modificar una plantilla y asignar el nombre Product Owner
        """
        print("\nProbando modificar una plantilla y asignar el nombre de Product Owner")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "Product Owner"
        }
        response = self.client.put("/api/plantillas/2/", plantilla, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_modificar_plantilla_con_nombre_existente_sh(self):
        """
        test_modificar_plantilla_con_nombre_existente_sh
        Prueba modificar una plantilla y asignar el nombre Stake Holder
        """
        print("\nProbando modificar una plantilla y asignar el nombre de Stake Holder")
        self.client.login(username="testing", password="polijira2021")
        plantilla = {
            "nombre": "Stake Holder"
        }
        response = self.client.put("/api/plantillas/1/", plantilla, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)
