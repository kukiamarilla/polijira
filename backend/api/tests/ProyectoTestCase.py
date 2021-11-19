import datetime
from django.test import TestCase, Client
from backend.api.models import Miembro, Proyecto, RolProyecto, Usuario, Permiso, PermisoProyecto, SprintBacklog
from backend.api.models.Sprint import Sprint
from backend.api.models.UserStory import UserStory


class ProyectoTestCase(TestCase):
    """
    ProyectoTestCase Prueba las funcionalidades del modelo Proyecto
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
        "backend/api/fixtures/testing/miembrosprints.json",
    ]

    def setUp(self):
        """
        setUp Configura el TestCase
        """
        self.client = Client()

    def test_listar_todos_los_proyectos_sin_permiso_ver_proyecto(self):
        """
        test_listar_proyectos_sin_permiso_ver_proyecto Prueba listar todos los proyectos al que es miembro el usuario
        """
        print("\nProbando listar todos los proyectos.")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(codigo="ver_proyectos").delete()
        response = self.client.get("/api/proyectos/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        usuario = Usuario.objects.get(pk=1)
        self.assertEquals(Proyecto.objects.filter(miembros__usuario=usuario).count(), len(body))

    def test_listar_todos_los_proyectos(self):
        """
        test_listar_todos_los_proyectos Prueba listar todos los proyectos del sistema
        """
        print("\nProbando listar todos los proyectos del sistema.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/proyectos/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Proyecto.objects.count(), len(body))

    def test_obtener_proyecto(self):
        """
        test_obtener_proyecto Prueba obtener detalles de un proyecto
        """
        print("\nProbando obtener detalles de un proyecto.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/proyectos/1/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        proyecto = Proyecto.objects.get(pk=1)
        self.assertEquals(body['nombre'], proyecto.nombre)
        self.assertEquals(body['fecha_inicio'], str(proyecto.fecha_inicio))
        self.assertEquals(body['fecha_fin'], str(proyecto.fecha_fin))
        self.assertEquals(body['scrum_master']['id'], proyecto.scrum_master.id)
        self.assertEquals(body['estado'], proyecto.estado)

    def test_obtener_proyecto_no_existente(self):
        """
        test_obtener_proyecto_no_existente Prueba obtener detalles de un proyecto que no existe
        """
        print("\nProbando obtener detalles de un proyecto que no existe")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/proyectos/1000/")
        body = response.json()
        self.assertEquals(body['error'], 'not_found')
        self.assertEquals(response.status_code, 404)

    def test_crear_proyecto(self):
        """
        test_crear_proyecto Prueba crear un proyecto
        """
        print("\nProbando crear un proyecto")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.post("/api/proyectos/", proyecto_body, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        proyecto = Proyecto.objects.filter(
            nombre=proyecto_body["nombre"],
            fecha_inicio=proyecto_body["fecha_inicio"],
            fecha_fin=proyecto_body["fecha_fin"],
            scrum_master=Usuario.objects.get(pk=proyecto_body["scrum_master_id"]),
            estado="P"
        )
        self.assertEquals(len(proyecto), 1)
        proyecto = proyecto[0]
        miembro = Miembro.objects.filter(
            usuario=proyecto.scrum_master,
            proyecto=proyecto,
            rol=RolProyecto.objects.get(nombre="Scrum Master", proyecto=proyecto)
        )
        self.assertEquals(len(miembro), 1)
        body = response.json()
        self.assertEquals(body["nombre"], proyecto.nombre)
        self.assertEquals(body["fecha_inicio"], str(proyecto.fecha_inicio))
        self.assertEquals(body["fecha_fin"], str(proyecto.fecha_fin))
        self.assertEquals(body["scrum_master"]["id"], proyecto.scrum_master.id)
        self.assertEquals(proyecto.estado, "P")

    def test_crear_proyecto_pasando_un_estado(self):
        """
        test_crear_proyecto_pasando_un_estado
        Prueba crear un proyecto pasando un estado que difiere de su estado inicial Pendiente
        """
        print("\nProbando crear un proyecto asignando un estado diferente a Pendiente")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2,
            "estado": "A"
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 200)
        proyecto = Proyecto.objects.filter(
            nombre=proyecto_body["nombre"],
            fecha_inicio=proyecto_body["fecha_inicio"],
            fecha_fin=proyecto_body["fecha_fin"],
            scrum_master=Usuario.objects.get(pk=proyecto_body["scrum_master_id"]),
        )
        self.assertEquals(len(proyecto), 1)
        proyecto = proyecto[0]
        self.assertEquals(proyecto.estado, "P")

    def test_crear_proyecto_sin_permiso_crear_proyectos(self):
        """
        test_crear_proyecto_sin_permiso_crear_proyectos Prueba crear un proyecto sin tener permiso de crear proyectos
        """
        print("\nProbando crear proyecto sin permiso crear proyectos")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(pk=11).delete()
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["crear_proyectos", "ver_usuarios"])
        self.assertEquals(body["error"], "forbidden")

    def test_crear_proyecto_sin_permiso_ver_usuarios(self):
        """
        test_crear_proyecto_sin_permiso_crear_proyectos Prueba crear un proyecto sin tener permiso de ver usuarios
        """
        print("\nProbando crear proyecto sin permiso ver usuarios")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(pk=1).delete()
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["crear_proyectos", "ver_usuarios"])
        self.assertEquals(body["error"], "forbidden")

    def test_crear_proyecto_con_sm_no_existente(self):
        """
        test_crear_proyecto_con_usuario_no_existente Prueba crear un proyecto con un Scrum Master que no existe
        """
        print("\nProbando crear proyecto con un scrum master que no existe")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 55
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_crear_proyecto_con_nombre_existente(self):
        """
        test_crear_proyecto_con_nombre_existente Prueba crear un proyecto con nombre ya existente
        """
        print("\nProbando crear un proyecto con nombre existente.")
        self.client.login(username="testing", password="polijira2021")
        Proyecto.objects.create(nombre="Proyecto A", fecha_inicio=datetime.date.today(),
                                fecha_fin=datetime.date.today() + datetime.timedelta(100), scrum_master_id=1)
        proyecto_body = {
            "nombre": "Proyecto A",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 1
        }
        response = self.client.post("/api/proyectos/", proyecto_body, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["nombre"], ["Ya existe un proyecto con ese nombre"])

    def test_crear_proyecto_con_campo_nombre_superando_max_length(self):
        """
        test_crear_proyecto_con_campo_nombre_superando_max_length
        Prueba crear un proyecto con un nombre que supera el limite máximo de caracteres
        """
        print("\nProbando crear un proyecto con un nombre que supere el max_length=255")
        self.client.login(username="testing", password="polijira2021")
        nombre_proyecto = ""
        for i in range(0, 256):
            nombre_proyecto += "a"
        proyecto_body = {
            "nombre": nombre_proyecto,
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)
        self.assertEquals(body["errors"]["nombre"], ["Sobrepasó el limite de caracteres"])

    def test_crear_proyecto_con_campo_nombre_no_asignado(self):
        """
        test_crear_proyecto_con_campo_nombre_no_asignado Prueba crear un proyecto sin especificar el campo nombre
        """
        print("\nProbando crear un proyecto sin asignar el campo nombre")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 3
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)
        self.assertEquals(body["errors"]["nombre"], ["No se especificó ningun nombre"])

    def test_crear_proyecto_con_campo_fecha_inicio_no_asignado(self):
        """
        test_crear_proyecto_con_campo_fecha_inicio_no_asignado
        Prueba crear un proyecto sin especificar el campo fecha de inicio
        """
        print("\nProbando crear un proyecto sin especificar el campo fecha de inicio")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 3
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)
        self.assertEquals(body["errors"]["fecha_inicio"], ["No se especificó ninguna fecha de inicio"])

    def test_crear_proyecto_con_campo_fecha_fin_no_asignado(self):
        """
        test_crear_proyecto_con_campo_fecha_inicio_no_asignado
        Prueba crear un proyecto sin especificar el campo fecha de fin
        """
        print("\nProbando crear un proyecto sin especificar el campo fecha de fin")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "scrum_master_id": 3
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)
        self.assertEquals(body["errors"]["fecha_fin"], ["No se especificó ninguna fecha de fin"])

    def test_crear_proyecto_con_campo_scrum_master_id_sin_especificar(self):
        """
        test_crear_proyecto_con_campo_scrum_master_id_sin_especificar
        Prueba crear un proyecto sin especificar al Scrum Master
        """
        print("\nProbando crear un proyecto sin especificar al Scrum Master")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)
        self.assertEquals(body["errors"]["scrum_master_id"], ["No se especificó el Scrum Master"])

    def test_modificar_proyecto(self):
        """
        test_modificar_proyecto Prueba modificar un proyecto
        """
        print("\nProbando modificar un proyecto")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestModificar",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 1
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 200)
        proyecto = Proyecto.objects.filter(
            nombre=proyecto_body["nombre"],
            fecha_inicio=proyecto_body["fecha_inicio"],
            fecha_fin=proyecto_body["fecha_fin"],
            scrum_master=Usuario.objects.get(pk=proyecto_body["scrum_master_id"])
        )
        self.assertEquals(len(proyecto), 1)
        proyecto = proyecto[0]
        miembro = Miembro.objects.filter(
            usuario=proyecto.scrum_master,
            proyecto=proyecto,
            rol=RolProyecto.objects.get(nombre="Scrum Master")
        )
        self.assertEquals(len(miembro), 1)
        body = response.json()
        self.assertEquals(proyecto.estado, "P")
        self.assertEquals(body["nombre"], proyecto.nombre)
        self.assertEquals(body["fecha_inicio"], str(proyecto.fecha_inicio))
        self.assertEquals(body["fecha_fin"], str(proyecto.fecha_fin))
        self.assertEquals(body["scrum_master"]["id"], proyecto.scrum_master.id)
        # TODO self.asserEquals(body["scrum_master"]["rol"]["nombre"], "Scrum Master")

    def test_modificar_proyecto_con_estado_activo(self):
        """
        test_modificar_proyecto_con_estado_activo Prueba modificar un proyecto en estado Activado
        """
        print("\nProbando modificar un proyecto en estado activado")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.estado = "A"
        proyecto.save()
        proyecto_body = {
            "nombre": "ProyectoTestModificar",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 1
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        body = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertEquals(body["error"], "bad_request")

    def test_modificar_proyecto_con_estado_finalizado(self):
        """
        test_modificar_proyecto_con_estado_finalizado Prueba modificar un proyecto en estado Finalizado
        """
        print("\nProbando modificar un proyecto en estado Finalizado")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.estado = "F"
        proyecto.save()
        proyecto_body = {
            "nombre": "ProyectoTestModificar",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 1
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        body = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertEquals(body["error"], "bad_request")

    def test_modificar_proyecto_con_estado_cancelado(self):
        """
        test_modificar_proyecto_con_estado_cancelado Prueba modificar un proyecto en estado Cancelado
        """
        print("\nProbando modificar un proyecto en estado Cancelado")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.estado = "C"
        proyecto.save()
        proyecto_body = {
            "nombre": "ProyectoTestModificar",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 1
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        body = response.json()
        self.assertEquals(response.status_code, 400)
        self.assertEquals(body["error"], "bad_request")

    def test_modificar_proyecto_sin_permiso_modificar_proyectos(self):
        """
        test_modificar_proyecto_sin_permiso_crear_proyectos
        Prueba modificar un proyecto sin tener permiso modificar proyectos
        """
        print("\nProbando modificar proyecto sin permiso crear proyectos")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(pk=12).delete()
        proyecto_body = {
            "nombre": "ProyectoTestModificar",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["modificar_proyectos", "ver_proyectos", "ver_usuarios"])
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_proyecto_sin_permiso_ver_proyectos(self):
        """
        test_modificar_proyecto_sin_permiso_ver_proyectos
        Prueba modificar un proyecto sin tener permiso ver proyectos
        """
        print("\nProbando modificar un proyecto sin permiso ver proyectos")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(pk=10).delete()
        proyecto_body = {
            "nombre": "ProyectoTestModificar",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["modificar_proyectos", "ver_proyectos", "ver_usuarios"])
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_proyecto_sin_permiso_ver_usuarios(self):
        """
        test_modificar_proyecto_sin_permiso_ver_proyectos
        Prueba modificar un proyecto sin tener permiso ver usuarios
        """
        print("\nProbando modificar un proyecto sin permiso ver proyectos")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(pk=1).delete()
        proyecto_body = {
            "nombre": "ProyectoTestModificar",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["modificar_proyectos", "ver_proyectos", "ver_usuarios"])
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_proyecto_con_nombre_existente(self):
        """
        test_modificar_proyecto_con_nombre_existente Prueba modificar un proyecto con nombre ya existente
        """
        print("\nProbando modificar un proyecto con nombre existente.")
        self.client.login(username="testing", password="polijira2021")
        Proyecto.objects.create(nombre="Proyecto A", fecha_inicio=datetime.date.today(),
                                fecha_fin=datetime.date.today() + datetime.timedelta(100), scrum_master_id=1)
        proyecto_body = {
            "nombre": "Proyecto A",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 1
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["message"], "Ya existe un proyecto con ese nombre")
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_proyecto_no_existente(self):
        """
        test_modificar_proyecto_no_existente Prueba modificar un proyecto que no existe
        """
        print("\nProbando modificar un proyecto que no existe")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestModificar",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.put("/api/proyectos/1000/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_modificar_proyecto_con_sm_no_existente(self):
        """
        test_modificar_proyecto_con_usuario_no_existente
        Prueba modificar un proyecto con un Scrum Master que no existe
        """
        print("\nProbando modificar proyecto con un scrum master que no existe")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 55
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_modificar_proyecto_con_campo_nombre_superando_max_length(self):
        """
        test_modificar_proyecto_con_campo_nombre_superando_max_length
        Prueba modificar un proyecto con un nombre que supera el limite máximo de caracteres
        """
        print("\nProbando modificar un proyecto con un nombre que supere el max_length=255")
        self.client.login(username="testing", password="polijira2021")
        nombre_proyecto = ""
        for i in range(0, 256):
            nombre_proyecto += "a"
        proyecto_body = {
            "nombre": nombre_proyecto,
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)
        self.assertEquals(body["errors"]["nombre"], ["Sobrepasó el limite de caracteres"])

    def test_modificar_proyecto_con_campo_nombre_no_asignado(self):
        """
        test_modificar_proyecto_con_campo_nombre_no_asignado
        Prueba modificar un proyecto sin especificar el campo nombre
        """
        print("\nProbando modificar un proyecto sin asignar el campo nombre")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 3
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)
        self.assertEquals(body["errors"]["nombre"], ["No se especificó ningun nombre"])

    def test_modificar_proyecto_con_campo_fecha_inicio_no_asignado(self):
        """
        test_modificar_proyecto_con_campo_fecha_inicio_no_asignado
        Prueba modificar un proyecto sin especificar el campo fecha de inicio
        """
        print("\nProbando modificar un proyecto sin especificar el campo fecha de inicio")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 3
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)
        self.assertEquals(body["errors"]["fecha_inicio"], ["No se especificó ninguna fecha de inicio"])

    def test_modificar_proyecto_con_campo_fecha_fin_no_asignado(self):
        """
        test_modificar_proyecto_con_campo_fecha_inicio_no_asignado
        Prueba modificar un proyecto sin especificar el campo fecha de fin
        """
        print("\nProbando modificar un proyecto sin especificar el campo fecha de fin")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "scrum_master_id": 3
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)
        self.assertEquals(body["errors"]["fecha_fin"], ["No se especificó ninguna fecha de fin"])

    def test_modificar_proyecto_con_campo_scrum_master_id_sin_especificar(self):
        """
        test_modificar_proyecto_con_campo_scrum_master_id_sin_especificar
        Prueba modificar un proyecto sin especificar al Scrum Master
        """
        print("\nProbando modificar un proyecto sin especificar al Scrum Master")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(len(body["errors"]), 1)
        self.assertEquals(body["errors"]["scrum_master_id"], ["No se especificó el Scrum Master"])

    def test_eliminar_proyecto(self):
        """
        test_eliminar_proyecto Prueba eliminar un proyecto
        """
        print("\nProbando eliminar un proyecto")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/proyectos/1/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(body["message"], "Proyecto Eliminado")

    def test_eliminar_proyecto_sin_permiso_eliminar_proyecto(self):
        """
        test_eliminar_proyecto_sin_permiso_eliminar_proyecto
        Prueba eliminar un proyecto sin tener permiso eliminar proyecto
        """
        print("\nProbando eliminar proyecto sin permiso eliminar proyecto")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(pk=13).delete()
        response = self.client.delete("/api/proyectos/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_proyectos", "eliminar_proyectos"])
        self.assertEquals(body["error"], "forbidden")

    def test_eliminar_proyecto_sin_permiso_ver_proyecto(self):
        """
        test_eliminar_proyecto_sin_permiso_ver_proyecto
        Prueba eliminar un proyecto sin tener permiso ver proyecto
        """
        print("\nProbando eliminar proyecto sin permiso ver proyecto")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(pk=13).delete()
        response = self.client.delete("/api/proyectos/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_proyectos", "eliminar_proyectos"])
        self.assertEquals(body["error"], "forbidden")

    def test_eliminar_proyecto_no_existente(self):
        """
        test_eliminar_proyecto_no_existente Prueba eliminar un proyecto que no existe
        """
        print("\nProbando eliminar un proyecto que no existe")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/proyectos/1000/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_eliminar_proyecto_con_estado_activo(self):
        """
        test_eliminar_proyecto_con_estado_activo Prueba eliminar un proyecto con estado Activado
        """
        print("\nProbando eliminar un proyecto con estado Activo")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.estado = "A"
        proyecto.save()
        response = self.client.delete("/api/proyectos/1/")
        self.assertEquals(response.status_code, 400)
        body = response.json()
        self.assertEquals(body["error"], "bad_request")

    def test_eliminar_proyecto_con_estado_cancelado(self):
        """
        test_eliminar_proyecto_con_estado_cancelado Prueba eliminar un proyecto con estado Cancelado
        """
        print("\nProbando eliminar un proyecto en estado Cancelado")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.estado = "C"
        proyecto.save()
        response = self.client.delete("/api/proyectos/1/")
        self.assertEquals(response.status_code, 400)
        body = response.json()
        self.assertEquals(body["error"], "bad_request")

    def test_eliminar_proyecto_con_estado_finalizado(self):
        """
        test_eliminar_proyecto_con_estado_finalizado Prueba eliminar un proyecto en estado Finalizado
        """
        print("\nProbando eliminar un proyecto en estado Finalizado")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.estado = "F"
        proyecto.save()
        response = self.client.delete("/api/proyectos/1/")
        self.assertEquals(response.status_code, 400)
        body = response.json()
        self.assertEquals(body["error"], "bad_request")

    def test_crear_proyecto_con_fecha_en_el_pasado(self):
        """
        test_crear_proyecto_con_fecha_en_el_pasado Prueba crear un proyecto con una fecha en el pasado
        """
        print("\nProbando crear proyecto con una fecha que este en el pasado")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": "1996-04-11",
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body["errors"]["fecha_inicio"], ["La fecha de inicio no puede estar en el pasado"])

    def test_crear_proyecto_con_fecha_fin_menor_a_fecha_inicio(self):
        """
        test_crear_proyecto_con_fecha_fin_menor_a_fecha_inicio
        Prueba crear un proyecto con una fecha de fin menor a la de inicio
        """
        print("\nProbando crear un proyecto con una fecha de fin menor a la de inicio")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() - datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body["errors"]["fecha_fin"], ["La fecha de fin no puede ser menor a la de inicio"])

    def test_modificar_proyecto_con_fecha_en_el_pasado(self):
        """
        test_modificar_proyecto_con_fecha_en_el_pasado Prueba modificar un proyecto con una fecha en el pasado
        """
        print("\nProbando modificar proyecto con una fecha que este en el pasado")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": "1996-04-11",
            "fecha_fin": datetime.date.today() + datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body["errors"]["fecha_inicio"], ["La fecha de inicio no puede estar en el pasado"])

    def test_modificar_proyecto_con_fecha_fin_menor_a_fecha_inicio(self):
        """
        test_modificar_proyecto_con_fecha_fin_menor_a_fecha_inicio
        Prueba modificar un proyecto con una fecha de fin menor a la de inicio
        """
        print("\nProbando modificar un proyecto con una fecha de fin menor a la de inicio")
        self.client.login(username="testing", password="polijira2021")
        proyecto_body = {
            "nombre": "ProyectoTestCrear",
            "fecha_inicio": datetime.date.today(),
            "fecha_fin": datetime.date.today() - datetime.timedelta(5),
            "scrum_master_id": 2
        }
        response = self.client.put("/api/proyectos/1/", proyecto_body, "application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body["errors"]["fecha_fin"], ["La fecha de fin no puede ser menor a la de inicio"])

    def test_activar_proyecto(self):
        """
        test_activar_proyecto Prueba activar un proyecto
        """
        print("\nProbando activar un proyecto")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/proyectos/1/activar/")
        self.assertEquals(response.status_code, 200)
        proyecto = Proyecto.objects.get(pk=1)
        self.assertEquals(proyecto.estado, "A")
        self.assertEquals(proyecto.fecha_inicio, datetime.date.today())

    def test_activar_proyecto_sin_permiso(self):
        """
        test_activar_proyecto_permiso activar un proyecto no teniendo el permiso activar_proyecto
        """
        print("\nProbando activar un proyecto sin ser Scrum Master")
        self.client.login(username="testing", password="polijira2021")
        rol = Miembro.objects.get(usuario_id=1, proyecto_id=1).rol
        rol.eliminar_permiso(PermisoProyecto.objects.get(codigo="activar_proyecto"))
        response = self.client.post("/api/proyectos/1/activar/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_activar_proyecto_no_existente(self):
        """
        test_activar_proyecto_no_existente Prueba activar un proyecto que no existe
        """
        print("\nProbando activar un proyecto que no existe")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/proyectos/1000/activar/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_activar_proyecto_cancelado(self):
        """
        test_activar_proyecto_activado Prueba activar un proyecto cancelado
        """
        print("\nProbando activar un proyecto cancelado")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.estado = "C"
        proyecto.save()
        response = self.client.post("/api/proyectos/1/activar/")
        self.assertEquals(response.status_code, 400)
        body = response.json()
        self.assertEquals(body["estado"], "Cancelado")
        self.assertEquals(body["error"], "bad_request")

    def test_activar_proyecto_finalizado(self):
        """
        test_activar_proyecto_activado Prueba activar un proyecto finalizado
        """
        print("\nProbando activar un proyecto finalizado")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.estado = "F"
        proyecto.save()
        response = self.client.post("/api/proyectos/1/activar/")
        self.assertEquals(response.status_code, 400)
        body = response.json()
        self.assertEquals(body["estado"], "Finalizado")
        self.assertEquals(body["error"], "bad_request")

    def test_obtener_proyecto_sin_ser_miembro_con_permiso_ver_proyectos(self):
        """
        test_obtener_proyecto_sin_ser_miembro_con_permiso_ver_proyectos
        Prueba obtener un proyecto sin ser miembro, pero teniendo permiso para ver proyectos
        """
        print("\nProbando obtener un proyecto sin ser miembro de ese proyecto y teniendo permiso para ver proyectos")
        self.client.login(username="testing", password="polijira2021")
        Miembro.objects.get(pk=1).delete()
        response = self.client.get("/api/proyectos/1/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        proyecto = Proyecto.objects.get(pk=1)
        self.assertEquals(body['nombre'], proyecto.nombre)
        self.assertEquals(body['fecha_inicio'], str(proyecto.fecha_inicio))
        self.assertEquals(body['fecha_fin'], str(proyecto.fecha_fin))
        self.assertEquals(body['scrum_master']['id'], proyecto.scrum_master.id)
        self.assertEquals(body['estado'], proyecto.estado)

    def test_obtener_proyecto_sin_permiso_ver_proyectos_siendo_miembro(self):
        """
        test_obtener_proyecto_sin_permiso_ver_proyectos_siendo_miembro
        Prueba obtener un proyecto sin permiso ver proyectos y siendo miembro de ese proyecto
        """
        print("\nProbando obtener un proyecto sin permiso ver proyectos y siendo miembro")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(codigo="ver_proyectos").delete()
        response = self.client.get("/api/proyectos/1/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        proyecto = Proyecto.objects.get(pk=1)
        self.assertEquals(body['nombre'], proyecto.nombre)
        self.assertEquals(body['fecha_inicio'], str(proyecto.fecha_inicio))
        self.assertEquals(body['fecha_fin'], str(proyecto.fecha_fin))
        self.assertEquals(body['scrum_master']['id'], proyecto.scrum_master.id)
        self.assertEquals(body['estado'], proyecto.estado)

    def test_obtener_proyecto_sin_permiso_ver_proyectos_no_siendo_miembro(self):
        """
        test_obtener_proyecto_sin_permiso_ver_proyectos_no_siendo_miembro
        Prueba obtener un proyecto sin tener permiso ver proyectos y sin ser miembro del proyecto
        """
        print("\nProbando obtener un proyecto sin ser miembro y tener permiso de ver proyectos")
        self.client.login(username="testing", password="polijira2021")
        Miembro.objects.get(pk=1).delete()
        Permiso.objects.get(codigo="ver_proyectos").delete()
        response = self.client.get("/api/proyectos/1/")
        self.assertEquals(response.status_code, 403)

    def test_obtener_estimaciones_pendientes(self):
        """
        test_obtener_estimaciones_pendientes
        Prueba obtener las estimaciones pendientes del Proyecto
        """
        print("\nProbando obtener las estimaciones pendientes del Proyecto.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.estado_estimacion = "p"
        sprint_backlog.save()
        usuario = Usuario.objects.get(pk=1)
        proyecto = Proyecto.objects.get(pk=3)
        miembro = Miembro.objects.get(usuario=usuario, proyecto=proyecto)
        us = SprintBacklog.objects.filter(estado_estimacion='p', desarrollador__miembro_proyecto=miembro)
        response = self.client.get("/api/proyectos/" + str(proyecto.id) + "/estimaciones_pendientes/")
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body), len(us))

    def test_obtener_estimaciones_pendientes_sin_ser_miembro(self):
        """
        test_obtener_estimaciones_pendientes_sin_ser_miembro
        Prueba obtener las estimaciones pendientes del Proyecto sin ser miembro
        """
        print("\nProbando obtener las estimaciones pendientes del Proyecto sin ser miembro.")
        self.client.login(username="user_test", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.estado_estimacion = "p"
        sprint_backlog.save()
        proyecto = Proyecto.objects.get(pk=3)
        response = self.client.get("/api/proyectos/" + str(proyecto.id) + "/estimaciones_pendientes/")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "Usted no es miembro de este Proyecto")
        self.assertEqual(body["error"], "forbidden")

    def test_obtener_estimaciones_pendientes_proyecto_inexistente(self):
        """
        test_obtener_estimaciones_pendientes_proyecto_inexistente
        Prueba obtener las estimaciones pendientes de Proyecto inexistente
        """
        print("\nProbando obtener las estimaciones pendientes de Proyecto inexistente.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(pk=1)
        sprint_backlog.estado_estimacion = "p"
        sprint_backlog.save()
        response = self.client.get("/api/proyectos/99/estimaciones_pendientes/")
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body["message"], "No existe el Proyecto")
        self.assertEqual(body["error"], "not_found")

    def test_finalizar_proyecto(self):
        """
        test_finalizar_proyecto
        Prueba finalizar un proyecto
        """
        print("\nProbando finalizar un proyecto.")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.iniciar()
        user_stories = UserStory.objects.filter(proyecto=proyecto)
        for user_story in user_stories:
            user_story.lanzar()
        sprints = Sprint.objects.filter(proyecto=proyecto)
        for sprint in sprints:
            sprint.finalizar()
        response = self.client.post("/api/proyectos/" + str(proyecto.id) + "/finalizar/")
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["estado"], "F")
        proyecto = Proyecto.objects.get(pk=1)
        self.assertEqual(proyecto.estado, "F")

    def test_finalizar_proyecto_sin_permiso_finalizar_proyecto(self):
        """
        test_finalizar_proyecto_sin_permiso
        Prueba finalizar un proyecto sin permiso
        """
        print("\nProbando finalizar un proyecto sin permiso.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="finalizar_proyecto").delete()
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.iniciar()
        user_stories = UserStory.objects.filter(proyecto=proyecto)
        for user_story in user_stories:
            user_story.lanzar()
        sprints = Sprint.objects.filter(proyecto=proyecto)
        for sprint in sprints:
            sprint.finalizar()
        response = self.client.post("/api/proyectos/" + str(proyecto.id) + "/finalizar/")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "No tiene permiso para realizar esta accion")
        self.assertEqual(body["error"], "forbidden")

    def test_finalizar_proyecto_no_iniciado(self):
        """
        test_finalizar_proyecto_no_iniciado
        Prueba finalizar un proyecto sin iniciar
        """
        print("\nProbando finalizar un proyecto sin iniciar.")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        user_stories = UserStory.objects.filter(proyecto=proyecto)
        for user_story in user_stories:
            user_story.lanzar()
        sprints = Sprint.objects.filter(proyecto=proyecto)
        for sprint in sprints:
            sprint.finalizar()
        response = self.client.post("/api/proyectos/" + str(proyecto.id) + "/finalizar/")
        body = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body["message"], "No puedes finalizar el Proyecto en su estado actual")
        self.assertEqual(body["error"], "bad_request")

    def test_finalizar_proyecto_sin_ser_miembro(self):
        """
        test_finalizar_proyecto_sin_ser_miembro
        Prueba finalizar un proyecto sin ser miembro
        """
        print("\nProbando finalizar un proyecto sin ser miembro.")
        self.client.login(username="user_test", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.iniciar()
        user_stories = UserStory.objects.filter(proyecto=proyecto)
        for user_story in user_stories:
            user_story.lanzar()
        sprints = Sprint.objects.filter(proyecto=proyecto)
        for sprint in sprints:
            sprint.finalizar()
        response = self.client.post("/api/proyectos/" + str(proyecto.id) + "/finalizar/")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "Usted no es miembro de este Proyecto")
        self.assertEqual(body["error"], "forbidden")

    def test_finalizar_proyecto_inexistente(self):
        """
        test_finalizar_proyecto_inexistente
        Prueba finalizar un proyecto inexistente
        """
        print("\nProbando finalizar un proyecto inexistente.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/proyectos/99/finalizar/")
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body["message"], "El proyecto no existe")
        self.assertEqual(body["error"], "not_found")

    def test_finalizar_proyecto_con_sprints_activos(self):
        """
        test_finalizar_proyecto_con_sprints_activos
        Prueba finalizar un proyecto con sprints activos
        """
        print("\nProbando finalizar un proyecto con sprints activos.")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.iniciar()
        user_stories = UserStory.objects.filter(proyecto=proyecto)
        for user_story in user_stories:
            user_story.lanzar()
        sprints = Sprint.objects.filter(proyecto=proyecto)
        for sprint in sprints:
            sprint.estado = "A"
            sprint.save()
        response = self.client.post("/api/proyectos/" + str(proyecto.id) + "/finalizar/")
        body = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            body["message"], "No puedes finalizar el Proyecto hasta que todos los Sprints esten finalizados")
        self.assertEqual(body["error"], "bad_request")

    def test_finalizar_proyecto_con_user_stories_pendientes(self):
        """
        test_finalizar_proyecto_con_user_stories_pendientes
        Prueba finalizar un proyecto con user stories pendientes
        """
        print("\nProbando finalizar un proyecto con user stories pendientes.")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.iniciar()
        user_stories = UserStory.objects.filter(proyecto=proyecto)
        for user_story in user_stories:
            user_story.estado = "P"
            user_story.save()
        sprints = Sprint.objects.filter(proyecto=proyecto)
        for sprint in sprints:
            sprint.finalizar()
        response = self.client.post("/api/proyectos/" + str(proyecto.id) + "/finalizar/")
        body = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            body["message"],
            "No puedes finalizar el Proyecto hasta que todos los User Stories esten lanzados o cancelados"
        )
        self.assertEqual(body["error"], "bad_request")

    def test_cancelar_proyecto(self):
        """
        test_cancelar_proyecto
        Prueba cancelar un proyecto
        """
        print("\nProbando cancelar un proyecto.")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.iniciar()
        response = self.client.post("/api/proyectos/" + str(proyecto.id) + "/cancelar/")
        sprint_activos = False
        sprints = Sprint.objects.filter(proyecto=proyecto)
        for sprint in sprints:
            if sprint.estado == "A":
                sprint_activos = True
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["estado"], "C")
        self.assertEqual(sprint_activos, False)
        proyecto = Proyecto.objects.get(pk=1)
        self.assertEqual(proyecto.estado, "C")

    def test_cancelar_proyecto_sin_ser_miembro(self):
        """
        test_cancelar_proyecto_sin_ser_miembro
        Prueba cancelar un proyecto sin ser miembro
        """
        print("\nProbando cancelar un proyecto sin ser miembro.")
        self.client.login(username="user_test", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.iniciar()
        response = self.client.post("/api/proyectos/" + str(proyecto.id) + "/cancelar/")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "Usted no es miembro de este Proyecto")
        self.assertEqual(body["error"], "forbidden")

    def test_cancelar_proyecto_inexistente(self):
        """
        test_cancelar_proyecto_inexistente
        Prueba cancelar un proyecto inexistente
        """
        print("\nProbando cancelar un proyecto inexistente.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/proyectos/99/cancelar/")
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body["message"], "El proyecto no existe")
        self.assertEqual(body["error"], "not_found")

    def test_cancelar_proyecto_sin_permiso_cancelar_proyecto(self):
        """
        test_cancelar_proyecto_sin_permiso_cancelar_proyecto
        Prueba cancelar un proyecto sin permisos
        """
        print("\nProbando cancelar un proyecto sin permisos.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="cancelar_proyecto").delete()
        proyecto = Proyecto.objects.get(pk=1)
        proyecto.iniciar()
        response = self.client.post("/api/proyectos/" + str(proyecto.id) + "/cancelar/")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEqual(body["error"], "forbidden")

    def test_cancelar_proyecto_no_activo(self):
        """
        test_cancelar_proyecto_no_activo
        Prueba cancelar un proyecto no activo
        """
        print("\nProbando cancelar un proyecto no activo.")
        self.client.login(username="testing", password="polijira2021")
        proyecto = Proyecto.objects.get(pk=1)
        response = self.client.post("/api/proyectos/" + str(proyecto.id) + "/cancelar/")
        body = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body["message"], "No puedes cancelar el Proyecto en su estado actual")
        self.assertEqual(body["error"], "bad_request")
