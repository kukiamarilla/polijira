import datetime
from backend.api.models import Proyecto, Usuario, Permiso
from django.test import TestCase, Client


class ProyectoTestCase(TestCase):
    """
    ProyectoTestCase Prueba las funcionalidades del modelo Proyecto
    """
    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
        "backend/api/fixtures/testing/permisos.json",
        "backend/api/fixtures/testing/roles.json",
        "backend/api/fixtures/testing/proyectos.json"
    ]

    def setUp(self):
        """
        setUp Configura el TestCase
        """
        self.client = Client()

    def test_listar_todos_los_proyectos(self):
        """
        test_listar_proyectos Prueba listar todos los proyectos si el usuario tiene el permiso para ver proyectos
        """
        print("\nProbando listar todos los proyectos.")
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
        scrum_master = Usuario.objects.get(pk=2)
        proyecto = Proyecto.objects.create(
            nombre="ProyectoTest",
            fecha_inicio=datetime.date.today(),
            fecha_fin=datetime.date.today() + datetime.timedelta(5),
            scrum_master=scrum_master
        )
        response = self.client.get("/api/proyectos/"+str(proyecto.id)+"/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body['nombre'], proyecto.nombre)
        self.assertEquals(body['fecha_inicio'], str(proyecto.fecha_inicio))
        self.assertEquals(body['fecha_fin'], str(proyecto.fecha_fin))
        self.assertEquals(body['scrum_master']['id'], proyecto.scrum_master.id)
        self.assertEquals(body['estado'], proyecto.estado)

    def test_obtener_proyecto_sin_permiso(self):
        """
        test_obtener_proyecto Prueba obtener detalles de un proyecto sin tener permiso para ver proyectos
        """
        print("\nProbando obtener detalles de un proyecto sin tener permiso.")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(pk=13).delete()
        scrum_master = Usuario.objects.get(pk=2)
        proyecto = Proyecto.objects.create(
            nombre="ProyectoTest",
            fecha_inicio=datetime.date.today(),
            fecha_fin=datetime.date.today() + datetime.timedelta(5),
            scrum_master=scrum_master
        )
        response = self.client.get("/api/proyectos/"+str(proyecto.id)+"/")
        body = response.json()
        self.assertEquals(body['permission_required'], ['ver_proyectos'])
        self.assertEquals(body['error'], 'forbidden')
        self.assertEquals(response.status_code, 403)

    def test_obtener_proyecto_no_existente(self):
        """
        test_obtener_proyecto_no_existente Prueba obtener detalles de un proyecto que no existe
        """
        print("\nProbando obtener detalles de un proyecto que no existe")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/proyectos/2/")
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
        response = self.client.post("/api/proyectos/", proyecto_body)
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
        body = response.json()
        self.assertEquals(body["nombre"], proyecto.nombre)
        self.assertEquals(body["fecha_inicio"], str(proyecto.fecha_inicio))
        self.assertEquals(body["fecha_fin"], str(proyecto.fecha_fin))
        self.assertEquals(body["scrum_master"]["id"], proyecto.scrum_master.id)
        self.assertEquals(proyecto.estado, "P")
        # TODO self.asserEquals(body["scrum_master"]["rol"]["nombre"], "Scrum Master")

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
        Permiso.objects.get(pk=10).delete()
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
            "scrum_master_id": 3
        }
        response = self.client.post("/api/proyectos/", proyecto_body)
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
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
        test_crear_proyecto_sin_permiso_crear_proyectos
        Prueba modificar un proyecto sin tener permiso modificar proyectos
        """
        print("\nProbando modificar proyecto sin permiso crear proyectos")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(pk=11).delete()
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
        Prueba modificar un proyecto sin tener permiso ver proyetos
        """
        print("\nProbando modificar un proyecto sin permiso ver proyectos")
        self.client.login(username="testing", password="polijira2021")
        Permiso.objects.get(pk=13).delete()
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
        Prueba modificar un proyecto sin tener permiso ver proyetos
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
        response = self.client.put("/api/proyectos/2/", proyecto_body, "application/json")
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
            "scrum_master_id": 3
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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
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
        Permiso.objects.get(pk=12).delete()
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
        response = self.client.delete("/api/proyectos/2/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_eliminar_proyecto_con_estado_activo(self):
        """
        test_eliminar_proyecto_con_estado_activoPrueba eliminar un proyecto con estado Activado
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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
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
        self.assertEquals(response.status_code, 400)
        body = response.json()
        self.assertEquals(body["errors"]["fecha_fin"], ["La fecha de fin no puede ser menor a la de inicio"])
