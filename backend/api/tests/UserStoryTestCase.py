from backend.api.models import Miembro, ProductBacklog, RegistroUserStory, UserStory, PermisoProyecto
from django.test import TestCase, Client
import datetime


class UserStoryTestCase(TestCase):
    """
    UserStoryTestCase Prueba las funcionalidades de User Story
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
        "backend/api/fixtures/testing/registro-user-stories.json"
    ]

    def setUp(self):
        """
        setUp Configura el TestCase
        """
        self.client = Client()

    def test_obtener_user_story(self):
        """
        obtener_user_story Prueba obtener los detalles de un User Story
        """
        print("\nProbando obtener los detalles de un User Story")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/user-stories/1/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        user_story = UserStory.objects.get(pk=1)
        self.assertEquals(body["id"], user_story.id)
        self.assertEquals(body["nombre"], user_story.nombre)
        self.assertEquals(body["descripcion"], user_story.descripcion)
        self.assertEquals(body["horas_estimadas"], user_story.horas_estimadas)
        self.assertEquals(body["prioridad"], user_story.prioridad)
        self.assertEquals(body["estado"], user_story.estado)
        self.assertEquals(body["fecha_release"], user_story.fecha_release)
        self.assertEquals(body["fecha_creacion"], str(user_story.fecha_creacion))
        self.assertEquals(body["desarrollador"], user_story.desarrollador)
        self.assertEquals(body["estado_estimacion"], user_story.estado_estimacion)
        self.assertEquals(body["product_backlog"], user_story.product_backlog)

    def test_obtener_user_story_no_existente(self):
        """
        test_obtener_user_story_no_existente Prueba obtener los detalles de un User Story que no existe en la BD
        """
        print("\nProbando obtener los detalles de un User Story que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/user-stories/1000/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_obtener_user_story_sin_permiso_ver_user_stories(self):
        """
        test_obtener_user_story_sin_permiso_ver_user_stories
        Prueba obtener los detalles de un User Story sin tener el permiso de proyecto: Ver User Stories
        """
        print("\nProbando obtener los detalles de un User Story sin tener permiso de proyecto Ver User Stories")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        response = self.client.get("/api/user-stories/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_listar_user_stories(self):
        """
        test_listar_user_stories Prueba listar todos los User Stories de un Proyecto
        """
        print("\nProbando listar todos los User Stories de un Proyecto")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/proyectos/1/user_stories/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(len(body), UserStory.objects.filter(product_backlogs__proyecto_id=1).count())

    def test_listar_user_stories_proyecto_no_existente(self):
        """
        test_listar_user_stories_proyecto_no_existente
        Prueba listar todos los User Stories de un Proyecto que no existe en la BD
        """
        print("\nProbando listar todos los User Stories de un Proyecto que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/proyectos/1000/user_stories/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_listar_user_story_sin_permiso_ver_user_stories(self):
        """
        test_obtener_user_story_sin_permiso_ver_user_stories
        Prueba listar los detalles de un User Story de un Proyecto sin tener el permiso de proyecto: Ver User Stories
        """
        print("\nProbando listar los detalles de un User Story sin tener permiso de proyecto Ver User Stories")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        response = self.client.get("/api/proyectos/1/user_stories/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_crear_user_story(self):
        """
        test_crear_user_story Prueba crear un User Story
        """
        print("\nProbando crear un User Story")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "proyecto": 2,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        user_story = UserStory.objects.filter(
            nombre=body["nombre"],
            descripcion=body["descripcion"],
            horas_estimadas=body["horas_estimadas"],
            prioridad=body["prioridad"],
            estado_estimacion=body["estado_estimacion"],
            fecha_creacion=body["fecha_creacion"],
            product_backlog=body["product_backlog"]
        )
        self.assertEquals(len(user_story), 1)
        user_story = user_story[0]
        self.assertEquals(user_story.fecha_creacion, datetime.date.today())
        self.assertEquals(user_story.product_backlog, True)
        product_backlog = ProductBacklog.objects.filter(
            proyecto_id=user_story_request["proyecto"],
            user_story=user_story
        )
        self.assertEquals(len(product_backlog), 1)
        registro = RegistroUserStory.objects.filter(
            nombre_antes=None,
            descripcion_antes=None,
            horas_estimadas_antes=None,
            prioridad_antes=None,
            estado_antes=None,
            desarrollador_antes=None,
            nombre_despues=user_story.nombre,
            descripcion_despues=user_story.descripcion,
            horas_estimadas_despues=user_story.horas_estimadas,
            prioridad_despues=user_story.prioridad,
            estado_despues=user_story.estado,
            desarrollador_despues=user_story.desarrollador,
            user_story=user_story,
            fecha=datetime.date.today(),
            accion="Creacion",
            autor_id=2
        )
        self.assertEquals(len(registro), 1)

    def test_crear_user_story_sin_permiso_crear_user_stories(self):
        """
        test_crear_user_story_sin_permiso_crear_user_stories
        Prueba crear un User Story sin tener el permiso de proyecto Crear User Stories
        """
        print("\nProbando crear un User Story sin tener permiso Crear User Stories")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="crear_user_stories").delete()
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "proyecto": 1,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["crear_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_crear_user_story_sin_ser_miembro(self):
        """
        test_crear_user_story_sin_ser_miembro Prueba crear un User Story sin ser miembro del proyecto
        """
        print("\nProbando crear un User Story sin ser miembro del proyecto")
        self.client.login(username="testing", password="polijira2021")
        Miembro.objects.get(pk=1).delete()
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "proyecto": 1,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_crear_user_story_sin_nombre(self):
        """
        test_crear_user_story_sin_nombre Prueba crear un User Story sin especificar nombre
        """
        print("\nProbando crear un User Story sin especificar nombre")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "proyecto": 1,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_crear_user_story_sin_descripcion(self):
        """
        test_crear_user_story_sin_descripcion Prueba crear un User Story sin especificar descripcion
        """
        print("\nProbando crear un User Story sin especificar descripcion")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "horas_estimadas": 20,
            "prioridad": 4,
            "proyecto": 1,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["descripcion"]), 1)

    def test_crear_user_story_sin_horas_estimadas(self):
        """
        test_crear_user_story_sin_horas_estimadas Prueba crear un User Story sin especificar horas estimadas
        """
        print("\nProbando crear un User Story sin especificar horas_estimadas")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "prioridad": 4,
            "proyecto": 1,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horas_estimadas"]), 1)

    def test_crear_user_story_sin_prioridad(self):
        """
        test_crear_user_story_sin_prioridad Prueba crear un User Story sin especificar prioridad
        """
        print("\nProbando crear un User Story sin especificar prioridad")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "proyecto": 1,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["prioridad"]), 1)

    def test_crear_user_story_sin_proyecto(self):
        """
        test_crear_user_story_sin_proyecto Prueba crear un User Story sin especificar proyecto
        """
        print("\nProbando crear un User Story sin especificar proyecto")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["proyecto"]), 1)

    def test_crear_user_story_sin_estado_estimacion(self):
        """
        test_crear_user_story_sin_estado_estimacion Prueba crear un User Story sin especificar estado estimacion
        """
        print("\nProbando crear un User Story sin especificar estado_estimacion")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "proyecto": 1
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["estado_estimacion"]), 1)

    def test_crear_user_story_max_length_nombre(self):
        """
        test_crear_user_story_max_length_nombre
        Prueba crear un User Story asignando un nombre superando la longitud máxima permitida
        """
        print("\nProbando crear un User Story asignando un nombre que supere la longitud máxima")
        self.client.login(username="testing", password="polijira2021")
        nombre = ""
        for i in range(0, 256):
            nombre += "a"
        user_story_request = {
            "nombre": nombre,
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "proyecto": 1,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_crear_user_story_hora_negativa(self):
        """
        test_crear_user_story_hora_negativa
        Prueba crear un User Story asignando una hora negativa
        """
        print("\nProbando crear un User Story asignando una hora negativa")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": -20,
            "prioridad": 4,
            "proyecto": 1,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horas_estimadas"]), 1)

    def test_crear_user_story_prioridad_mayor_10(self):
        """
        test_crear_user_story_prioridad_mayor_10 Prueba crear un User Story asignando una prioridad mayor a 10
        """
        print("\nProbando crear un User Story con una prioridad mayor a 10")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 14,
            "proyecto": 1,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["prioridad"]), 1)

    def test_crear_user_story_prioridad_negativa(self):
        """
        test_crear_user_story_prioridad_negativa Prueba crear un User Story asignando una prioridad negativa
        """
        print("\nProbando crear un User Story con una prioridad negativa")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": -14,
            "proyecto": 1,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["prioridad"]), 1)

    def test_crear_user_story_proyecto_no_existente(self):
        """
        test_crear_user_story_proyecto_no_existente Prueba crear un User Story asignando un proyecto que no existe
        """
        print("\nProbando crear un User Story con un proyecto que no existe")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 8,
            "proyecto": 1000,
            "estado_estimacion": "P"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["proyecto"]), 1)

    def test_crear_user_story_estado_estimacion_incorrecto(self):
        """
        test_crear_user_story_estado_estimacion_incorrecto
        Prueba crear un User Story con un estado estimacion que no sea N, P o C
        """
        print("\nProbando crear un User Story con un estado estimacion que no sea N, P o C")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 8,
            "proyecto": 1,
            "estado_estimacion": "d"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["estado_estimacion"]), 1)

    def test_crear_user_story_estado_estimacion_max_length_mayor_a_1(self):
        """
        test_crear_user_story_estado_estimacion_max_length_mayor_a_1
        Prueba crear un User Story con un estado estimacion que no tenga solo un caracter
        """
        print("\nProbando crear un User Story con un estado estimacion que tenga mas de un caracter")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 8,
            "proyecto": 1,
            "estado_estimacion": "holiiii"
        }
        response = self.client.post("/api/user-stories/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["estado_estimacion"]), 1)

    def test_modificar_user_story_caso_1(self):
        """
        test_modificar_user_story Prueba modificar un User Story cuando solo tiene el registro de su creacion
        """
        print("\nProbando modificar un User Story que tiene solo un registro")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USModificar_caso_1",
            "descripcion": "Modificar caso 1: El US tiene solo un registro",
            "horas_estimadas": 20,
            "prioridad": 8,
            "estado_estimacion": "N"
        }
        user_story_antes = UserStory.objects.get(pk=1)
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        user_story = UserStory.objects.get(pk=1)
        self.assertEquals(body["id"], user_story.id)
        self.assertEquals(user_story_request["nombre"], user_story.nombre)
        self.assertEquals(user_story_request["descripcion"], user_story.descripcion)
        self.assertEquals(user_story_request["horas_estimadas"], user_story.horas_estimadas)
        self.assertEquals(user_story_request["prioridad"], user_story.prioridad)
        self.assertEquals(user_story_request["estado_estimacion"], user_story.estado_estimacion)
        registro = RegistroUserStory.objects.filter(
            nombre_antes=user_story_antes.nombre,
            descripcion_antes=user_story_antes.descripcion,
            horas_estimadas_antes=user_story_antes.horas_estimadas,
            prioridad_antes=user_story_antes.prioridad,
            estado_antes=user_story_antes.estado,
            desarrollador_antes=user_story_antes.desarrollador,
            nombre_despues=user_story.nombre,
            descripcion_despues=user_story.descripcion,
            horas_estimadas_despues=user_story.horas_estimadas,
            prioridad_despues=user_story.prioridad,
            estado_despues=user_story.estado,
            desarrollador_despues=user_story.desarrollador,
            user_story=user_story,
            fecha=datetime.date.today(),
            accion="Modificacion",
            autor_id=1
        )
        self.assertEquals(len(registro), 1)

    def test_modificar_user_story_caso_2(self):
        """
        test_modificar_user_story_caso_2
        Prueba modificar un User Story que tiene varios registros (sin eliminacion)
        """
        print("\nProbando modificar un User Story que tiene varios registros")
        self.client.login(username="testing", password="polijira2021")
        user_story = UserStory.objects.get(pk=1)
        user_story.update(
            nombre="USTestModificar_caso_2",
            descripcion="Modificar caso 2",
            horas_estimadas=5,
            prioridad=10,
            estado_estimacion="C",
            autor=Miembro.objects.get(pk=1),
            registro_handler=RegistroUserStory.modificar_registro
        )
        user_story_request = {
            "nombre": "USModificar_caso_2",
            "descripcion": "Caso 2: Modificacion con varios registros",
            "horas_estimadas": 20,
            "prioridad": 8,
            "estado_estimacion": "N"
        }
        user_story_antes = user_story
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        user_story = UserStory.objects.get(pk=1)
        self.assertEquals(body["id"], user_story.id)
        self.assertEquals(user_story_request["nombre"], user_story.nombre)
        self.assertEquals(user_story_request["descripcion"], user_story.descripcion)
        self.assertEquals(user_story_request["horas_estimadas"], user_story.horas_estimadas)
        self.assertEquals(user_story_request["prioridad"], user_story.prioridad)
        self.assertEquals(user_story_request["estado_estimacion"], user_story.estado_estimacion)
        registro = RegistroUserStory.objects.filter(
            nombre_antes=user_story_antes.nombre,
            descripcion_antes=user_story_antes.descripcion,
            horas_estimadas_antes=user_story_antes.horas_estimadas,
            prioridad_antes=user_story_antes.prioridad,
            estado_antes=user_story_antes.estado,
            desarrollador_antes=user_story_antes.desarrollador,
            nombre_despues=user_story.nombre,
            descripcion_despues=user_story.descripcion,
            horas_estimadas_despues=user_story.horas_estimadas,
            prioridad_despues=user_story.prioridad,
            estado_despues=user_story.estado,
            desarrollador_despues=user_story.desarrollador,
            user_story=user_story,
            fecha=datetime.date.today(),
            accion="Modificacion",
            autor_id=1
        )
        self.assertEquals(len(registro), 1)

    def test_modificar_user_story_no_existente(self):
        """
        test_modificar_user_story_no_existente Prueba modificar un User Story que no existe en la BD
        """
        print("\nProbando modificar un User Story que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 8,
            "estado_estimacion": "N"
        }
        response = self.client.put("/api/user-stories/1000/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_modificar_user_story_no_siendo_miembro(self):
        """
        test_modificar_user_story_no_siendo_miembro Prueba modificar un User Story no siendo miembro del Proyecto
        """
        print("\nProbando modificar un User Story no siendo miembro del Proyecto")
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.get(pk=1)
        miembro.usuario_id = 2
        miembro.save()
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_user_story_con_estado_release(self):
        """
        test_modificar_user_story_con_estado_release Prueba modificar un User Story que tiene estado liberado
        """
        print("\nProbando modificar un User Story que tiene estado liberado")
        self.client.login(username="testing", password="polijira2021")
        user_story = UserStory.objects.get(pk=1)
        user_story.lanzar()
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_modificar_user_story_con_estado_cancelado(self):
        """
        test_modificar_user_story_con_estado_cancelado Prueba modificar un User Story que tiene el estado Cancelado
        """
        print("\nProbando modificar un User Story que tiene estado Cancelado")
        self.client.login(username="testing", password="polijira2021")
        user_story = UserStory.objects.get(pk=1)
        user_story.cancelar()
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_modificar_user_story_sin_permiso_ver_user_stories(self):
        """
        test_modificar_user_story_sin_permiso_ver_user_stories
        Prueba modificar un User Story sin tener el permiso de proyecto: Ver User Stories
        """
        print("\nProbando modificar un User Story sin tener permiso de proyecto Ver User Stories")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_user_stories", "modificar_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_user_story_sin_permiso_modificar_user_stories(self):
        """
        test_modificar_user_story_sin_permiso_modificar_user_stories
        Prueba modificar un User Story sin tener el permiso de proyecto: Modificar User Stories
        """
        print("\nProbando modificar un User Story sin tener permiso de proyecto Modificar User Stories")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="modificar_user_stories").delete()
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_user_stories", "modificar_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_user_story_sin_nombre(self):
        """
        test_modificar_user_story_sin_nombre Prueba modificar un User Story sin especificar nombre
        """
        print("\nProbando modificar un User Story sin especificar nombre")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_modificar_user_story_sin_descripcion(self):
        """
        test_modificar_user_story_sin_descripcion Prueba modificar un User Story sin especificar descripcion
        """
        print("\nProbando modificar un User Story sin especificar descripcion")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "horas_estimadas": 20,
            "prioridad": 4,
            "estado_estimacion": "C"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["descripcion"]), 1)

    def test_modificar_user_story_sin_horas_estimadas(self):
        """
        test_modificar_user_story_sin_horas_estimadas Prueba modificar un User Story sin especificar horas estimadas
        """
        print("\nProbando modificar un User Story sin especificar horas_estimadas")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "prioridad": 4,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horas_estimadas"]), 1)

    def test_modificar_user_story_sin_prioridad(self):
        """
        test_modificar_user_story_sin_prioridad Prueba modificar un User Story sin especificar prioridad
        """
        print("\nProbando modificar un User Story sin especificar prioridad")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["prioridad"]), 1)

    def test_modificar_user_story_sin_estado_estimacion(self):
        """
        test_modificar_user_story_sin_estado_estimacion
        Prueba modificar un User Story sin especificar estado estimacion
        """
        print("\nProbando modificar un User Story sin especificar estado_estimacion")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["estado_estimacion"]), 1)

    def test_modificar_user_story_max_length_nombre(self):
        """
        test_modificar_user_story_max_length_nombre
        Prueba modificar un User Story asignando un nombre superando la longitud máxima permitida
        """
        print("\nProbando modificar un User Story asignando un nombre que supere la longitud máxima")
        self.client.login(username="testing", password="polijira2021")
        nombre = ""
        for i in range(0, 256):
            nombre += "a"
        user_story_request = {
            "nombre": nombre,
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 4,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["nombre"]), 1)

    def test_modificar_user_story_hora_negativa(self):
        """
        test_modificar_user_story_hora_negativa
        Prueba modificar un User Story asignando una hora negativa
        """
        print("\nProbando modificar un User Story asignando una hora negativa")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": -20,
            "prioridad": 4,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["horas_estimadas"]), 1)

    def test_modificar_user_story_prioridad_mayor_10(self):
        """
        test_modificar_user_story_prioridad_mayor_10 Prueba modificar un User Story asignando una prioridad mayor a 10
        """
        print("\nProbando modificar un User Story con una prioridad mayor a 10")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 14,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["prioridad"]), 1)

    def test_modificar_user_story_prioridad_negativa(self):
        """
        test_modificar_user_story_prioridad_negativa Prueba modificar un User Story asignando una prioridad negativa
        """
        print("\nProbando modificar un User Story con una prioridad negativa")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": -14,
            "estado_estimacion": "P"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["prioridad"]), 1)

    def test_modificar_user_story_estado_estimacion_incorrecto(self):
        """
        test_modificar_user_story_estado_estimacion_incorrecto
        Prueba modificar un User Story con un estado estimacion que no sea N, P o C
        """
        print("\nProbando modificar un User Story con un estado estimacion que no sea N, P o C")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 8,
            "estado_estimacion": "d"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["estado_estimacion"]), 1)

    def test_modificar_user_story_estado_estimacion_max_length_mayor_a_1(self):
        """
        test_modificar_user_story_estado_estimacion_max_length_mayor_a_1
        Prueba modificar un User Story con un estado estimacion que no tenga solo un caracter
        """
        print("\nProbando modificar un User Story con un estado estimacion que tenga mas de un caracter")
        self.client.login(username="testing", password="polijira2021")
        user_story_request = {
            "nombre": "USTest",
            "descripcion": "Esto es una descripcion",
            "horas_estimadas": 20,
            "prioridad": 8,
            "estado_estimacion": "holiiii"
        }
        response = self.client.put("/api/user-stories/1/", user_story_request, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]["estado_estimacion"]), 1)

    def test_eliminar_user_story(self):
        """
        test_eliminar_user_story Prueba eliminar un User Story
        """
        print("\nProbando eliminar un User Story")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/user-stories/1/")
        self.assertEquals(response.status_code, 200)
        user_story = UserStory.objects.get(pk=1)
        self.assertEquals(user_story.estado, "E")
        self.assertEquals(user_story.product_backlog, False)
        product_backlog = ProductBacklog.objects.filter(user_story=user_story)
        self.assertEquals(len(product_backlog), 0)
        registro = RegistroUserStory.objects.filter(
            user_story=user_story,
            accion="Eliminacion",
            autor_id=1,
            fecha=datetime.date.today()
        )
        self.assertEquals(len(registro), 1)
        registro = registro[0]
        self.assertEquals(registro.nombre_antes, user_story.nombre)
        self.assertEquals(registro.descripcion_antes, user_story.descripcion)
        self.assertEquals(registro.horas_estimadas_antes, user_story.horas_estimadas)
        self.assertEquals(registro.prioridad_antes, user_story.prioridad)
        self.assertEquals(registro.estado_antes, user_story.estado)
        self.assertEquals(registro.desarrollador_antes, user_story.desarrollador)
        self.assertEquals(registro.nombre_despues, None)
        self.assertEquals(registro.descripcion_despues, None)
        self.assertEquals(registro.horas_estimadas_despues, None)
        self.assertEquals(registro.prioridad_despues, None)
        self.assertEquals(registro.estado_despues, None)
        self.assertEquals(registro.desarrollador_despues, None)

    def test_eliminar_user_story_no_existente(self):
        """
        test_eliminar_user_story_no_existente Prueba eliminar un User Story que no existe en la BD
        """
        print("\nProbando eliminar un User Story que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/user-stories/1000/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_eliminar_user_story_no_siendo_miembro(self):
        """
        test_eliminar_user_story_no_siendo_miembro Prueba eliminar un User Story no siendo miembro del Proyecto
        """
        print("\nProbando eliminar un User Story no siendo miembro del Proyecto")
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.get(pk=1)
        miembro.usuario_id = 2
        miembro.save()
        response = self.client.delete("/api/user-stories/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_eliminar_user_story_que_no_esta_en_pb(self):
        """
        test_eliminar_user_story_que_no_esta_en_pb
        Prueba eliminar un User Story que no se encuentra en el Product Backlog
        """
        print("\nProbando eliminar un User Story que no se encuentra en el Product Backlog")
        self.client.login(username="testing", password="polijira2021")
        user_story = UserStory.objects.get(pk=1)
        user_story.product_backlog = False
        user_story.save()
        response = self.client.delete("/api/user-stories/1/")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_eliminar_user_story_sin_permiso_ver_user_stories(self):
        """
        test_ver_user_story_sin_permiso_ver_user_stories
        Prueba eliminar un User Story sin tener permiso de proyecto: Ver User Stories
        """
        print("\nProbando eliminar un User Story sin tener permiso de ver user stories")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        response = self.client.delete("/api/user-stories/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")
        self.assertEquals(body["permission_required"], ["ver_user_stories", "eliminar_user_stories"])

    def test_eliminar_user_story_sin_permiso_eliminar_user_stories(self):
        """
        test_eliminar_user_story_sin_permiso_eliminar_user_stories
        Prueba eliminar un User Story sin tener permiso de proyecto: Eliminar User Stories
        """
        print("\nProbando eliminar un User Story sin tener permiso de eliminar user stories")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="eliminar_user_stories").delete()
        response = self.client.delete("/api/user-stories/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")
        self.assertEquals(body["permission_required"], ["ver_user_stories", "eliminar_user_stories"])

    def test_listar_registros(self):
        """
        test_listar_registros Prueba listar todos los registros de un User Story
        """
        print("\nProbando listar todos los registros de un User Story")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/user-stories/1/registros/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(len(body), RegistroUserStory.objects.filter(user_story_id=1).count())

    def test_listar_registros_de_us_no_existente(self):
        """
        test_listar_registros_de_us_no_existente Prueba listar los registros de un User Story que no existe en la BD
        """
        print("\nProbando listar los registros de un User Story que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/user-stories/1000/registros/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_listar_registros_de_us_sin_permiso_ver_user_stories(self):
        """
        test_listar_registros_de_us_sin_permiso_ver_user_stories
        Prueba listar los registros de un User Story sin tener el permiso de proyecto: Ver User Stories
        """
        print("\nProbando listar los registros de un User Story sin tener permiso de proyecto Ver User Stories")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        response = self.client.get("/api/user-stories/1/registros/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_user_stories"])
        self.assertEquals(body["error"], "forbidden")