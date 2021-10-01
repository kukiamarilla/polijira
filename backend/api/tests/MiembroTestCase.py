from backend.api.models.Proyecto import Proyecto
from backend.api.models.Usuario import Usuario
from django.test import TestCase
from django.test import Client
from backend.api.models import Miembro, RolProyecto


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

    def test_obtener_miembro(self):
        """
        test_obtener_miembro Prueba obtener un miembro
        """
        print("\nProbando obtener un miembro.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/2/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        miembro = Miembro.objects.get(pk=2)
        self.assertEquals(body["id"], miembro.id)
        self.assertEquals(body["usuario"]["id"], miembro.usuario.id)
        self.assertEquals(body["proyecto"]["id"], miembro.proyecto.id)
        self.assertEquals(body["rol"]["id"], miembro.rol.id)

    def test_obtener_miembro_sin_ser_miembro_proyecto(self):
        """
        test_obtener_miembro_sin_ser_miembro_proyecto
        Prueba obtener un miembro sin ser miembro del proyecto del miembro especificado
        """
        print("\nProbando obtener un miembro sin ser miembro del proyecto del miembro especificado.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/3/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "Usted no es miembro de este proyecto")

    def test_obtener_miembro_sin_permiso(self):
        """
        test_obtener_miembro_sin_permiso Prueba obtener un miembro sin permiso
        """
        print("\nProbando obtener un miembro sin permiso.")
        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="ver_miembros")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/2/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_miembros"])

    def test_obtener_miembro_no_existente(self):
        """
        test_obtener_miembro Prueba obtener un miembro que no existe
        """
        print("\nProbando obtener un miembro que no existe.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/999/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["error"], "not_found")

    def test_crear_miembro(self):
        """
        test_crear_miembro Prueba crear un miembro
        """
        print("\nProbando crear un miembro.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        usuario = Usuario.objects.get(pk=request_data["usuario"])
        proyecto = Proyecto.objects.get(pk=request_data["proyecto"])
        rol = RolProyecto.objects.get(pk=request_data["rol"])
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

    def test_crear_miembro_sin_ser_miembro_proyecto(self):
        """
        test_crear_miembro_sin_ser_miembro_proyecto Prueba crear un miembro sin ser miembro del proyecto especificado
        """
        print("\nProbando crear un miembro sin ser miembro del proyecto especificado.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 4,
            "proyecto": 2,
            "horario": {
                "lunes": 1,
                "martes": 2,
                "miercoles": 3,
                "jueves": 4,
                "viernes": 5,
                "sabado": 2,
                "domingo": 2
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "Usted no es miembro de este proyecto")

    def test_crear_miembro_sin_permiso_agregar_miembros(self):
        """
        test_crear_miembro_sin_permiso_agregar_miembros Prueba crear un miembro sin permiso agregar miembros
        """
        print("\nProbando crear un miembro sin permiso agregar miembros.")
        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="agregar_miembros")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": 2,
                "miercoles": 3,
                "jueves": 4,
                "viernes": 5,
                "sabado": 2,
                "domingo": 2
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["agregar_miembros", "ver_roles_proyecto", "ver_usuarios"])

    def test_crear_miembro_sin_permiso_ver_roles_proyecto(self):
        """
        test_crear_miembro_sin_permiso_ver_roles_proyecto Prueba crear un miembro sin permiso ver roles proyecto
        """
        print("\nProbando crear un miembro sin permiso ver roles proyecto.")
        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="ver_roles_proyecto")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": 2,
                "miercoles": 3,
                "jueves": 4,
                "viernes": 5,
                "sabado": 2,
                "domingo": 2
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["agregar_miembros", "ver_roles_proyecto", "ver_usuarios"])

    def test_crear_miembro_sin_permiso_ver_usuarios(self):
        """
        test_crear_miembro_sin_permiso_ver_usuarios Prueba crear un miembro sin permiso ver usuarios
        """
        print("\nProbando crear un miembro sin permiso ver usuarios.")
        rol = Usuario.objects.get(nombre="testing").rol
        permiso = rol.permisos.get(codigo="ver_usuarios")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": 2,
                "miercoles": 3,
                "jueves": 4,
                "viernes": 5,
                "sabado": 2,
                "domingo": 2
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["agregar_miembros", "ver_roles_proyecto", "ver_usuarios"])

    def test_crear_miembro_con_rol_scrum_master(self):
        """
        test_crear_miembro_con_rol_scrum_master Prueba crear un miembro con rol Scrum Master
        """
        print("\nProbando crear un miembro con rol Scrum Master.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 1,
            "proyecto": 1,
            "horario": {
                "lunes": 1,
                "martes": 2,
                "miercoles": 3,
                "jueves": 4,
                "viernes": 5,
                "sabado": 2,
                "domingo": 2
            }
        }
        response = self.client.post("/api/miembros/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["rol"], ["El rol de Scrum Master no es asignable"])

    def test_crear_miembro_rol_distinto(self):
        """
        test_crear_miembro_rol_distinto Prueba crear un miembro con un rol que no pertenece al proyecto
        """
        print("\nProbando crear un miembro con un rol que no pertenece al proyecto.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 4,
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
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["rol"], ["El rol no pertenece a este proyecto"])

    def test_crear_miembro_con_usuario_ya_agregado(self):
        """
        test_crear_miembro_con_usuario_ya_agregado Prueba crear un miembro
        con un usuario ya agregado al proyecto especificado
        """
        print("\nProbando crear un miembro con un usuario ya agregado al proyecto especificado.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 1,
            "rol": 3,
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
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["miembro"], ["Ya existe el miembro"])

    def test_crear_miembro_usuario_no_existente(self):
        """
        test_crear_miembro_usuario_no_existente Prueba crear un miembro con un usuario que no existe
        """
        print("\nProbando crear miembro con un usuario que no existe.")
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
        print("\nProbando crear miembro con un proyecto que no existe.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        self.assertEquals(body["errors"]["proyecto"], ["No se encontro un proyecto en la base de datos"])
        self.assertEquals(body["errors"]["rol"], ["El rol no pertenece a este proyecto"])

    def test_crear_miembro_rol_no_existente(self):
        """
        test_crear_miembro_rol_no_existente Prueba crear un miembro con un rol que no existe
        """
        print("\nProbando crear miembro con un rol que no existe.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
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
        self.assertEquals(body["errors"]["rol"], ["No se encontro un rol en la base de datos"])

    def test_crear_miembro_existente(self):
        """
        test_crear_mismo_miembro Prueba crear un miembro que ya existe
        """
        print("\nProbando crear un miembro que ya existe.")
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
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["miembro"], ["Ya existe el miembro"])

    def test_hora_mayor_a_24_lunes(self):
        """
        test_hora_mayor_a_24_lunes Prueba crear miembro con un horario pasando una hora superior a 24
        """
        print("\nProbando crear miembro con un horario con una hora superior a 24 - lunes.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora superior a 24 - martes.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora superior a 24 - miercoles.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora superior a 24 - jueves.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora superior a 24 - viernes.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora superior a 24 - sabado.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora superior a 24 - domingo.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora negativa - lunes.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora negativa - martes.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora negativa - miercoles.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora negativa - jueves.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora negativa - viernes.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora negativa - sabado.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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
        print("\nProbando crear miembro con un horario con una hora negativa - domingo.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "usuario": 3,
            "rol": 3,
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

    def test_eliminar_miembro(self):
        """
        test_eliminar_miembro Prueba eliminar un miembro
        """
        print("\nProbando eliminar un miembro.")
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.create(
            usuario=Usuario.objects.get(pk=3),
            proyecto=Proyecto.objects.get(pk=1),
            rol=RolProyecto.objects.get(pk=3)
        )
        response = self.client.delete("/api/miembros/" + str(miembro.id) + "/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["message"], "Miembro Eliminado")

    def test_eliminar_miembro_sin_permiso_eliminar_miembros(self):
        """
        test_eliminar_miembro_sin_permiso_eliminar_miembros Prueba eliminar un miembro sin permiso eliminar miembros
        """
        print("\nProbando eliminar un miembro sin permiso eliminar miembros.")
        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="eliminar_miembros")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.create(
            usuario=Usuario.objects.get(pk=3),
            proyecto=Proyecto.objects.get(pk=1),
            rol=RolProyecto.objects.get(pk=3)
        )
        response = self.client.delete("/api/miembros/" + str(miembro.id) + "/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        miembro_cant = Miembro.objects.filter(pk=miembro.pk)
        self.assertEquals(miembro_cant.count(), 1)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["eliminar_miembros", "ver_roles_proyecto", "ver_usuarios"])
        self.assertEquals(body["error"], "forbidden")

    def test_eliminar_miembro_sin_permiso_ver_roles_proyecto(self):
        """
        test_eliminar_miembro_sin_permiso_ver_roles_proyecto
        Prueba eliminar un miembro sin permiso ver roles de proyecto
        """
        print("\nProbando eliminar un miembro sin tener permiso de ver roles de proyecto.")
        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="ver_roles_proyecto")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.create(
            usuario=Usuario.objects.get(pk=3),
            proyecto=Proyecto.objects.get(pk=1),
            rol=RolProyecto.objects.get(pk=3)
        )
        response = self.client.delete("/api/miembros/" + str(miembro.id) + "/")
        body = response.json()
        miembro_cant = Miembro.objects.filter(pk=miembro.pk)
        self.assertEquals(response.status_code, 403)
        self.assertEquals(miembro_cant.count(), 1)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["eliminar_miembros", "ver_roles_proyecto", "ver_usuarios"])
        self.assertEquals(body["error"], "forbidden")

    def test_eliminar_miembro_sin_permiso_ver_usuarios(self):
        """
        test_eliminar_miembro_sin_permiso_ver_usuarios
        Prueba eliminar un miembro sin permiso ver usuarios
        """
        print("\nProbando eliminar un miembro sin tener permiso ver usuarios.")
        rol = Usuario.objects.get(nombre="testing").rol
        permiso = rol.permisos.get(codigo="ver_usuarios")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.create(
            usuario=Usuario.objects.get(pk=3),
            proyecto=Proyecto.objects.get(pk=1),
            rol=RolProyecto.objects.get(pk=3)
        )
        response = self.client.delete("/api/miembros/" + str(miembro.id) + "/")
        body = response.json()
        miembro_cant = Miembro.objects.filter(pk=miembro.pk)
        self.assertEquals(response.status_code, 403)
        self.assertEquals(miembro_cant.count(), 1)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["eliminar_miembros", "ver_roles_proyecto", "ver_usuarios"])
        self.assertEquals(body["error"], "forbidden")

    def test_eliminar_miembro_sin_ser_miembro_proyecto(self):
        """
        test_eliminar_miembro_sin_ser_miembro_proyecto
        Prueba eliminar un miembro sin ser miembro del proyecto del miembro especificado
        """
        print("\nProbando eliminar un miembro sin ser miembro del proyecto del miembro especificado.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/miembros/3/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "Usted no es miembro de este proyecto")

    def test_eliminar_mi_mismo_miembro(self):
        """
        test_eliminar_mi_mismo_miembro Prueba eliminar su mismo miembro
        """
        print("\nProbando eliminar el miembro al que pertenezco.")
        usuario = Usuario.objects.get(nombre="testing")
        proyecto = Proyecto.objects.get(pk=1)
        miembro = Miembro.objects.get(usuario=usuario, proyecto=proyecto)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/miembros/" + str(miembro.id) + "/")
        self.assertEquals(response.status_code, 400)
        body = response.json()
        self.assertEquals(body["error"], "bad_request")

    def test_eliminar_miembro_no_existente(self):
        """
        test_eliminar_miembro Prueba eliminar un miembro que no existe
        """
        print("\nProbando eliminar un miembro que no existe.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/miembros/1000/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el miembro")
        self.assertEquals(body["error"], "not_found")

    def test_modificar_miembro(self):
        """
        test_modificar_miembro Prueba modificar un miembro
        """
        print("\nProbando modificar un miembro.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 3
        }
        miembro = Miembro.objects.get(pk=2)
        response = self.client.put("/api/miembros/" + str(miembro.id) + "/",
                                   request_data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        miembro = Miembro.objects.get(pk=2)
        self.assertEquals(miembro.rol.id, body["rol"]["id"], request_data["rol"])

    def test_modificar_miembro_sin_permiso_modificar_miembros(self):
        """
        test_modificar_miembro_sin_permiso_modificar_miembros
        Prueba modificar un miembro sin permiso modificar miembros
        """
        print("\nProbando modificar un miembro sin permiso modificar miembros.")
        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="modificar_miembros")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 3
        }
        miembro_ant = Miembro.objects.get(pk=2)
        response = self.client.put("/api/miembros/2/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        miembro = Miembro.objects.get(pk=2)
        self.assertEquals(miembro.rol, miembro_ant.rol)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["modificar_miembros", "ver_roles_proyecto", "ver_usuarios"])

    def test_modificar_miembro_sin_permiso_ver_roles_proyecto(self):
        """
        test_modificar_miembro_sin_permiso_ver_roles_proyecto
        Prueba modificar un miembro sin permiso ver roles proyectos
        """
        print("\nProbando modificar un miembro sin permiso ver roles proyecto.")
        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="ver_roles_proyecto")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 3
        }
        miembro_ant = Miembro.objects.get(pk=2)
        response = self.client.put("/api/miembros/2/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        miembro = Miembro.objects.get(pk=2)
        self.assertEquals(miembro.rol, miembro_ant.rol)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["modificar_miembros", "ver_roles_proyecto", "ver_usuarios"])

    def test_modificar_miembro_sin_permiso_ver_usuarios(self):
        """
        test_modificar_miembro_sin_permiso_ver_usuarios Prueba modificar un miembro sin permiso ver usuarios
        """
        print("\nProbando modificar un miembro sin permiso ver usuarios.")
        rol = Usuario.objects.get(nombre="testing").rol
        permiso = rol.permisos.get(codigo="ver_usuarios")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 3
        }
        miembro_ant = Miembro.objects.get(pk=2)
        response = self.client.put("/api/miembros/2/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        miembro = Miembro.objects.get(pk=2)
        self.assertEquals(miembro.rol, miembro_ant.rol)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["modificar_miembros", "ver_roles_proyecto", "ver_usuarios"])

    def test_modificar_miembro_rol_distinto(self):
        """
        test_modificar_miembro_rol_distinto Prueba modificar un miembro con un rol que no pertenece al proyecto
        """
        print("\nProbando modificar un miembro con un rol que no pertenece al proyecto.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 4
        }
        response = self.client.put("/api/miembros/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["message"], "El rol no pertenece a este proyecto")
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_miembro_sin_ser_miembro_proyecto(self):
        """
        test_modificar_miembro_sin_ser_miembro_proyecto
        Prueba modificar un miembro sin ser miembro del proyecto del miembro especificado
        """
        print("\nProbando modificar un miembro sin ser miembro del proyecto del miembro especificado.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 3
        }
        response = self.client.put("/api/miembros/3/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "Usted no es miembro de este proyecto")

    def test_modificar_miembro_rol_no_existente(self):
        """
        test_modificar_miembro_rol_no_existente Prueba modificar un miembro pasando un rol que no existe
        """
        print("\nProbando modificar un miembro con un rol que no existe.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 2000
        }
        response = self.client.put("/api/miembros/1/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(len(body["errors"]["rol"]), 1)

    def test_modificar_miembro_no_existente(self):
        """
        test_modificar_miembro_no_existente Prueba modificar un miembro que no existe
        """
        print("\nProbando modificar un miembro que no existe.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 2
        }
        response = self.client.put("/api/miembros/1000/", request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el miembro")
        self.assertEquals(body["error"], "not_found")

    def test_modificar_miembro_a_rol_scrum_master(self):
        """
        test_modificar_miembro_a_rol_scrum_master Prueba modificar un miembro pasando el rol de Scrum Master
        """
        print("\nProbando modificar un miembro pasando el rol de Scrum Master.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "rol": 1
        }
        response = self.client.put("/api/miembros/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["rol"]), 1)
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["rol"], ["No puedes asignar el rol Scrum Master"])

    def test_obtener_horario(self):
        """
        test_obtener_horario Prueba obtener un horario de un miembro
        """
        print("\nProbando obtener un horario de un miembro.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/1/horario/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        horario_db = Miembro.objects.get(pk=1).horario
        self.assertEquals(body["id"], horario_db.id)

    def test_obtener_horario_sin_ser_miembro_proyecto(self):
        """
        test_obtener_horario_sin_ser_miembro_proyecto
        Prueba obtener horario sin ser miembro del proyecto del miembro especificado
        """
        print("\nProbando obtener horario sin ser miembro del proyecto del miembro especificado.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/3/horario/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["message"], "Usted no es miembro de este proyecto")

    def test_obtener_horario_sin_permiso_ver_miembros(self):
        """
        test_obtener_horario_sin_permiso_ver_miembros Prueba obtener un horario sin permiso ver miembros
        """
        print("\nProbando obtener un horario sin tener permiso ver miembros.")
        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="ver_miembros")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/1/horario/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["error"], "forbidden")
        self.assertEquals(body["message"], "No tiene permiso para realizar esta accion")
        self.assertEquals(body["permission_required"], ["ver_miembros"])

    def test_obtener_horario_de_miembro_no_existente(self):
        """
        test_obtener_horario_de_miembro_no_existente Prueba obtener un horario de un miembro que no existe
        """
        print("\nProbando obtener un horario de un miembro que no existe.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/miembros/1000/horario/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")
