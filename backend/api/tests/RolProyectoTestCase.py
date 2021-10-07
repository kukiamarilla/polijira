from backend.api.models.PermisoProyecto import PermisoProyecto
from backend.api.models.Proyecto import Proyecto
from backend.api.models import RolProyecto, Miembro, Usuario
from django.test import TestCase, Client
from django.db.models import Q


class RolProyectoTestCase(TestCase):
    """
    RolProyectoTestCase Prueba las funcionalidades de Rol de Proyecto
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
        "backend/api/fixtures/testing/permisos.json",
        "backend/api/fixtures/testing/roles.json",
        "backend/api/fixtures/testing/permisosProyecto.json",
        "backend/api/fixtures/testing/proyectos.json",
        "backend/api/fixtures/testing/plantillas.json",
        "backend/api/fixtures/testing/rolesProyecto.json",
        "backend/api/fixtures/testing/miembros.json"
    ]

    def setUp(self):
        """
        setUp Configura el testcase
        """
        self.client = Client()

    def test_obtener_rol_proyecto(self):
        """
        test_obtener_rol_proyecto Prueba la obtención de un rol de proyecto
        """
        print("\nProbando obtener un rol de proyecto.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles-proyecto/1/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        rol = RolProyecto.objects.get(pk=1)
        self.assertEquals(rol.nombre, body["nombre"])

    def test_obtener_rol_proyecto_sin_permiso(self):
        """
        test_obtener_rol_proyecto_sin_permiso Prueba la obtención de un rol de proyecto sin permiso
        """
        print("\nProbando obtener un rol de proyecto sin permiso.")
        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="ver_roles_proyecto")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles-proyecto/2/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        rol = RolProyecto.objects.get(pk=1)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_roles_proyecto", "ver_permisos_proyecto"])

    def test_obtener_rol_proyecto_inexistente(self):
        """
        test_obtener_rol_proyecto_inexistente Prueba la obtención de un rol de proyecto inexistente
        """
        print("\nProbando obtener un rol de proyecto no existente.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles-proyecto/666/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["message"], "No existe el rol de proyecto")

    def test_crear_rol_proyecto(self):
        """
        test_crear_rol_proyecto Prueba la creación de un rol de proyecto
        """
        print("\nProbando crear un rol de proyecto.")
        rol = {
            "nombre": "Rol Proyecto A",
            "permisos": [
                {
                    "id": 1
                },
                {
                    "id": 2
                }
            ],
            "proyecto": 1
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/roles-proyecto/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        rol_db = RolProyecto.objects.filter(Q(proyecto=1) and
                                            Q(permisos__id=1) and
                                            Q(permisos__id=2) and
                                            Q(nombre=rol["nombre"]))
        self.assertEquals(len(rol_db), 1)
        self.assertEquals(rol_db[0].nombre, body["nombre"])
        self.assertEquals(rol_db[0].permisos.count(), len(body["permisos"]))

    def test_crear_rol_proyecto_sin_permiso(self):
        """
        test_crear_rol_proyecto_sin_permiso Prueba la creación de un rol de proyecto sin permiso
        """
        print("\nProbando crear un rol de proyecto sin permiso.")
        rol_body = {
            "nombre": "Rol B",
            "permisos": [
                {
                    "id": 1
                },
                {
                    "id": 9
                }
            ],
            "proyecto": 1
        }

        usuario = Usuario.objects.get(nombre="testing")
        proyecto = Proyecto.objects.get(pk=rol_body["proyecto"])
        rol = Miembro.objects.get(usuario=usuario, proyecto=proyecto).rol
        permiso = rol.permisos.get(codigo="ver_permisos_proyecto")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/roles-proyecto/", rol_body, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['crear_roles_proyecto', 'ver_permisos_proyecto'])

    def test_crear_rol_proyecto_sin_agregar_permisos(self):
        """
        test_crear_rol_proyecto_sin_agregar_permisos Prueba la creación de un rol de proyecto sin permisos agregados
        """
        print("\nProbando crear un rol de proyecto sin permisos agregados.")
        rol = {
            "nombre": "Rol Proyecto X",
            "permisos": [],
            "proyecto": 1
        }
        self.client.login(username="testing", password="polijira2021")
        roles_cant = RolProyecto.objects.count()
        response = self.client.post("/api/roles-proyecto/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["errors"]["permisos"], ["Se debe especificar al menos un permiso"])
        rol_db = RolProyecto.objects.filter(Q(proyecto=1) and Q(nombre=rol["nombre"]))
        self.assertEquals(len(rol_db), 0)
        self.assertEquals(RolProyecto.objects.count(), roles_cant)

    def test_crear_rol_proyecto_con_permisos_inexistentes(self):
        """
        test_crear_rol_proyecto_con_permisos_inexistentes Prueba la creación de un
        rol de proyecto con permisos inexistentes
        """
        print("\nProbando crear un rol de proyecto con permisos inexistentes.")
        rol = {
            "nombre": "Rol Proyecto X",
            "permisos": [
                {
                    "id": 1
                },
                {
                    "id": 99
                }
            ],
            "proyecto": 1
        }
        self.client.login(username="testing", password="polijira2021")
        roles_cant = RolProyecto.objects.count()
        response = self.client.post("/api/roles-proyecto/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["errors"]["permisos"], ["No se encontró algunos de los permisos especificados"])
        rol_db = RolProyecto.objects.filter(Q(proyecto=1) and
                                            Q(permisos__id=1) and
                                            Q(permisos__id=99) and
                                            Q(nombre=rol["nombre"]))
        self.assertEquals(len(rol_db), 0)
        self.assertEquals(RolProyecto.objects.count(), roles_cant)

    def test_crear_rol_proyecto_sin_proyecto_agregado(self):
        """
        test_crear_rol_proyecto_sin_proyecto_agregado Prueba la creación de un rol de proyecto sin proyecto agregado
        """
        print("\nProbando crear un rol de proyecto sin proyecto agregado.")
        rol = {
            "nombre": "Rol Proyecto X",
            "permisos": [
                {
                    "id": 1
                }
            ],
            "proyecto": None
        }
        self.client.login(username="testing", password="polijira2021")
        roles_cant = RolProyecto.objects.count()
        response = self.client.post("/api/roles-proyecto/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["errors"]["proyecto"], ["Se debe especificar un proyecto"])
        rol_db = RolProyecto.objects.filter(nombre=rol["nombre"])
        self.assertEquals(len(rol_db), 0)
        self.assertEquals(RolProyecto.objects.count(), roles_cant)

    def test_crear_rol_proyecto_con_proyecto_inexistente(self):
        """
        test_crear_rol_proyecto_con_proyecto_inexistente Prueba la creación
        de un rol de proyecto con proyecto inexistente
        """
        print("\nProbando crear un rol de proyecto con proyecto inexistente.")
        rol = {
            "nombre": "Rol Proyecto X",
            "permisos": [
                {
                    "id": 1
                }
            ],
            "proyecto": 88
        }
        self.client.login(username="testing", password="polijira2021")
        roles_cant = RolProyecto.objects.count()
        response = self.client.post("/api/roles-proyecto/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["errors"]["proyecto"], ["No se encontró el proyecto especificado"])
        rol_db = RolProyecto.objects.filter(Q(proyecto=1) and
                                            Q(permisos__id=1) and
                                            Q(permisos__id=99) and
                                            Q(nombre=rol["nombre"]))
        self.assertEquals(len(rol_db), 0)
        self.assertEquals(RolProyecto.objects.count(), roles_cant)

    def test_eliminar_rol_proyecto(self):
        """
        test_eliminar_rol_proyecto Prueba la eliminación de un rol de proyecto
        """
        print("\nProbando eliminar un rol de proyecto.")
        self.client.login(username="testing", password="polijira2021")
        roles_cant = RolProyecto.objects.count()
        response = self.client.delete("/api/roles-proyecto/3/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["message"], "Rol de Proyecto Eliminado.")
        rol_db = RolProyecto.objects.filter(pk=3)
        self.assertEquals(len(rol_db), 0)
        self.assertEquals(RolProyecto.objects.count(), roles_cant - 1)

    def test_eliminar_rol_proyecto_sin_permiso(self):
        """
        test_eliminar_rol_proyecto_sin_permiso Prueba la eliminación de un rol de proyecto sin permiso
        """
        print("\nProbando eliminar un rol de proyecto sin permiso.")

        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="eliminar_roles_proyecto")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/roles-proyecto/2/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['ver_roles_proyecto', 'eliminar_roles_proyecto'])

    def test_eliminar_rol_proyecto_asignado_a_un_miembro(self):
        """
        test_eliminar_rol_proyecto_asignado_a_un_miembro Prueba eliminar un rol de proyecto asignado a un miembro
        """
        print("\nProbando eliminar un rol de proyecto asignado a un miembro.")
        self.client.login(username="testing", password="polijira2021")
        roles_cant = RolProyecto.objects.count()
        response = self.client.delete("/api/roles-proyecto/2/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "Rol asignado a un miembro de proyecto, no se puede eliminar")
        self.assertEquals(RolProyecto.objects.count(), roles_cant)

    def test_eliminar_rol_proyecto_inexistente(self):
        """
        test_eliminar_rol_proyecto_inexistente Prueba la eliminación de un rol de proyecto inexistente
        """
        print("\nProbando eliminar un rol de proyecto inexistente.")
        self.client.login(username="testing", password="polijira2021")
        roles_cant = RolProyecto.objects.count()
        response = self.client.delete("/api/roles-proyecto/99/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol de proyecto")
        self.assertEquals(RolProyecto.objects.count(), roles_cant)

    def test_modificar_rol_proyecto(self):
        """
        test_modificar_rol_proyecto Prueba la modificación de un rol de proyecto
        """
        print("\nProbando modificar un rol de proyecto.")
        rol = {
            "nombre": "Tirano"
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.put("/api/roles-proyecto/2/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        rol_db = RolProyecto.objects.filter(Q(nombre=rol["nombre"]) and Q(pk=2))
        self.assertEquals(len(rol_db), 1)
        self.assertEquals(rol_db[0].nombre, body["nombre"])

    def test_modificar_rol_proyecto_sin_permiso(self):
        """
        test_modificar_rol_proyecto_sin_permiso Prueba la modificación de un rol de proyecto sin permiso
        """
        print("\nProbando modificar un rol de proyecto sin permiso.")
        rol_body = {
            "nombre": "Tirano"
        }

        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="modificar_roles_proyecto")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.put("/api/roles-proyecto/2/", rol_body, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['ver_permisos_proyecto',
                          'ver_roles_proyecto', 'modificar_roles_proyecto'])

    def test_modificar_mi_propio_rol(self):
        """
        test_modificar_mi_propio_rol Prueba la modificación de mi propio rol
        """
        print("\nProbando la modificación de mi propio rol.")
        rol = {
            "nombre": "Dictador"
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.put("/api/roles-proyecto/1/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No puedes modificar tu propio rol")

    def test_modificar_rol_proyecto_inexistente(self):
        """
        test_modificar_rol_proyecto_inexistente Prueba la modificación de un rol de proyecto inexistente
        """
        print("\nProbando modificar un rol de proyecto inexistente.")
        rol = {
            "nombre": "Dictador"
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.put("/api/roles-proyecto/99/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol de proyecto")

    def test_listar_permisos_de_rol_proyecto(self):
        """
        test_listar_permisos_de_rol_proyecto Prueba el listado de permisos de un rol de proyecto
        """
        print("\nProbando listar permisos de un rol de proyecto.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles-proyecto/1/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(isinstance(body, list), True)
        rol = RolProyecto.objects.get(pk=1)
        self.assertEquals(rol.permisos.count(), len(body))

    def test_listar_permisos_de_rol_proyecto_sin_permiso(self):
        """
        test_listar_permisos_de_rol_proyecto_sin_permiso Prueba el listado de permisos de un rol de proyecto
        """
        print("\nProbando listar permisos de un rol de proyecto sin permiso.")

        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="ver_roles_proyecto")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles-proyecto/2/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['ver_roles_proyecto'])

    def test_listar_permisos_de_rol_proyecto_inexistente(self):
        """
        test_listar_permisos_de_rol_proyecto_inexistente Prueba el listado de permisos
        de un rol de proyecto inexistente
        """
        print("\nProbando listar permisos de un rol de proyecto inexistente.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles-proyecto/99/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol de proyecto")

    def test_agregar_permiso_a_rol_proyecto(self):
        """
        test_agregar_permiso_a_rol_proyecto Prueba agregar un permiso a un rol de proyecto
        """
        print("\nProbando agregar un permiso a un rol de proyecto.")
        permiso = {
            "id": 5
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/roles-proyecto/2/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        rol_db = RolProyecto.objects.filter(Q(permisos__id=permiso["id"]) and Q(pk=2))
        self.assertEquals(len(rol_db), 1)
        self.assertEquals(rol_db[0].permisos.count(), len(body["permisos"]))

    def test_agregar_permiso_a_rol_proyecto_sin_permiso(self):
        """
        test_agregar_permiso_a_rol_proyecto_sin_permiso Prueba agregar un permiso a un rol de proyecto sin permiso
        """
        print("\nProbando agregar un permiso a un rol de proyecto sin permiso.")
        permiso = {
            "id": 13
        }
        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="modificar_roles_proyecto")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/roles-proyecto/2/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['ver_permisos_proyecto', 'modificar_roles_proyecto'])

    def test_agregar_permiso_a_rol_proyecto_propio(self):
        """
        test_agregar_permiso_a_rol_proyecto_propio Prueba agregar un permiso a un rol de proyecto propio
        """
        print("\nProbando agregar un permiso a un rol de proyecto propio.")
        rol = RolProyecto.objects.get(pk=1)
        p = PermisoProyecto.objects.get(pk=31)
        rol.eliminar_permiso(p)
        permiso = {
            "id": 31
        }
        self.client.login(username="testing", password="polijira2021")
        permisos_cant = RolProyecto.objects.get(pk=1).permisos.count()
        response = self.client.post("/api/roles-proyecto/1/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No puedes modificar tu propio rol")
        rol = RolProyecto.objects.get(pk=1)
        self.assertEquals(rol.permisos.count(), permisos_cant)

    def test_agregar_permiso_a_rol_proyecto_inexistente(self):
        """
        test_agregar_permiso_a_rol_proyecto_inexistente Prueba agregar un permiso a un rol de proyecto inexistente
        """
        print("\nProbando agregar un permiso a un rol de proyecto inexistente.")
        permiso = {
            "id": 2
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/roles-proyecto/99/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol de proyecto")

    def test_agregar_permiso_inexistente_a_rol_proyecto(self):
        """
        test_agregar_permiso_inexistente_a_rol_proyecto Prueba agregar un permiso inexistente a un rol de proyecto
        """
        print("\nProbando agregar un permiso inexistente a un rol de proyecto.")
        permiso = {
            "id": 88
        }
        self.client.login(username="testing", password="polijira2021")
        permisos_cant = RolProyecto.objects.get(pk=2).permisos.count()
        response = self.client.post("/api/roles-proyecto/2/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["errors"]["id"], ["No existe el permiso de proyecto en la base de datos"])
        rol = RolProyecto.objects.get(pk=2)
        self.assertEquals(rol.permisos.count(), permisos_cant)

    def test_eliminar_permiso_a_rol_proyecto(self):
        """
        test_eliminar_permiso_a_rol_proyecto Prueba eliminar un permiso a un rol de proyecto
        """
        print("\nProbando eliminar un permiso a un rol de proyecto.")
        permiso = {
            "id": 11
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/roles-proyecto/2/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        rol = RolProyecto.objects.get(pk=2)
        self.assertEquals(rol.nombre, body["nombre"])
        self.assertEquals(rol.permisos.count(), len(body["permisos"]))

    def test_eliminar_todos_los_permisos_a_rol_proyecto(self):
        """
        test_eliminar_todos_los_permisos_a_rol_proyecto Prueba eliminar todos los permisos de un rol de proyecto
        """
        print("\nProbando eliminar todos los permisos de un rol de proyecto.")
        permiso = {
            "id": 1
        }
        p = Proyecto.objects.get(pk=1)
        rol = RolProyecto.objects.create(nombre="Rolcito", proyecto=p)
        rol.agregar_permiso(permiso["id"])
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/roles-proyecto/"+str(rol.pk)+"/permisos/",
                                      permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "El rol de proyecto no se puede quedar sin permisos")
        self.assertEquals(rol.permisos.all().count(), 1)

    def test_eliminar_permiso_a_rol_proyecto_sin_permiso(self):
        """
        test_eliminar_permiso_a_rol_proyecto_sin_permiso Prueba eliminar un permiso a un rol de proyecto sin permiso
        """
        print("\nProbando eliminar un permiso a un rol de proyecto sin permiso.")
        permiso = {
            "id": 1
        }

        usuario = Usuario.objects.get(nombre="testing")
        rol = RolProyecto.objects.get(pk=1)
        rol = Miembro.objects.get(usuario=usuario, proyecto=rol.proyecto).rol
        permiso = rol.permisos.get(codigo="modificar_roles_proyecto")
        rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/roles-proyecto/1/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['ver_permisos_proyecto', 'modificar_roles_proyecto'])

    def test_eliminar_permiso_a_rol_proyecto_propio(self):
        """
        test_eliminar_permiso_a_rol_proyecto_propio Prueba eliminar un permiso a un rol de proyecto propio
        """
        print("\nProbando eliminar un permiso a un rol de proyecto propio.")
        permiso = {
            "id": 22
        }
        self.client.login(username="testing", password="polijira2021")
        permisos_cant = RolProyecto.objects.get(pk=1).permisos.count()
        response = self.client.delete("/api/roles-proyecto/1/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No puedes modificar tu propio rol")
        rol = RolProyecto.objects.get(pk=1)
        self.assertEquals(rol.permisos.count(), permisos_cant)

    def test_eliminar_permiso_a_rol_proyecto_inexistente(self):
        """
        test_eliminar_permiso_a_rol_proyecto_inexistente Prueba eliminar un permiso a un rol de proyecto inexistente
        """
        print("\nProbando eliminar un permiso a un rol de proyecto inexistente.")
        permiso = {
            "id": 2
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/roles-proyecto/99/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol de proyecto")

    def test_eliminar_permiso_inexistente_a_rol_proyecto(self):
        """
        test_eliminar_permiso_inexistente_a_rol_proyecto Prueba eliminar un permiso inexistente a un rol de proyecto
        """
        print("\nProbando eliminar un permiso inexistente a un rol de proyecto.")
        permiso = {
            "id": 88
        }
        self.client.login(username="testing", password="polijira2021")
        rol = RolProyecto.objects.get(pk=2)
        permisos_cant = rol.permisos.count()
        response = self.client.delete("/api/roles-proyecto/2/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el permiso de proyecto")
        self.assertEquals(rol.permisos.count(), permisos_cant)

    def test_crear_rol_proyecto_sin_nombre(self):
        """
        test_crear_rol_proyecto_sin_nombre Prueba crear un rol de proyecto sin especificar el nombre
        """
        print("\nProbando crear un rol de proyecto sin especificar el nombre.")
        self.client.login(username="testing", password="polijira2021")
        rol = {
            "permisos": [
                {
                    "id": 1
                },
                {
                    "id": 2
                }
            ],
            "proyecto": 1
        }
        response = self.client.post("/api/roles-proyecto/", rol, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body["errors"]["nombre"], ["No se especificó ningun nombre"])

    def test_crear_rol_proyecto_con_nombre_superior_a_max_length(self):
        """
        test_crear_rol_proyecto_con_nombre_superior_a_max_length
        Prueba crear un rol de proyecto superando el límite máximo de caracteres
        """
        print("\nProbando crear un rol de proyecto superando el límite máximo de caracteres.")
        self.client.login(username="testing", password="polijira2021")
        nombre = ""
        for i in range(0, 256):
            nombre += "A"
        rol = {
            "nombre": nombre,
            "permisos": [
                {
                    "id": 1
                },
                {
                    "id": 2
                }
            ]
        }
        response = self.client.post("/api/roles-proyecto/", rol, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body["errors"]["nombre"], ["El nombre superó el máximo número de caracteres"])

    def test_modificar_rol_proyecto_sin_especificar_nombre(self):
        """
        test_modificar_rol_proyecto_sin_especificar_nombre Prueba modificar
        un rol de proyecto sin especificar el campo nombre
        """
        print("\nProbando modificar un rol de proyecto sin especificar el campo nombre.")
        self.client.login(username="testing", password="polijira2021")
        rol = {
            "permisos": [
                {
                    "id": 1
                },
                {
                    "id": 2
                }
            ]
        }
        response = self.client.put("/api/roles-proyecto/2/", rol, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        body = response.json()
        self.assertEquals(body["errors"]["nombre"], ["No se especificó ningun nombre"])
