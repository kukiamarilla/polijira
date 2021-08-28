from backend.api.models.Permiso import Permiso
from backend.api.models.Rol import Rol
from django.test import TestCase, Client
from django.db.models import Q


class RolTestCase(TestCase):
    """
    RolTestCase Prueba las funcionalidades de Roles
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
        "backend/api/fixtures/testing/permisos.json",
        "backend/api/fixtures/testing/roles.json",
    ]

    def setUp(self):
        """
        setUp Configura el testcase
        """
        self.client = Client()

    def test_listar_roles(self):
        """
        test_listar_roles Prueba el listado de todos los roles de sistema
        """
        print("\nProbando listar roles de sistema.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(isinstance(body, list), True)
        self.assertEquals(Rol.objects.count(), len(body))

    def test_obtener_rol(self):
        """
        test_obtener_rol Prueba la obtención de un rol de sistema
        """
        print("\nProbando obtener un rol de sistema.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles/1/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        rol = Rol.objects.get(pk=1)
        self.assertEquals(rol.nombre, body["nombre"])

    def test_obtener_rol_inexistente(self):
        """
        test_obtener_rol_inexistente Prueba la obtención de un rol de sistema inexistente
        """
        print("\nProbando obtener un rol de sistema no existente.")

        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles/99/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["message"], "No existe el rol")

    def test_crear_rol(self):
        """
        test_crear_rol Prueba la creación de un rol de sistema
        """
        print("\nProbando crear un rol de sistema.")
        rol = {
            "nombre": "Rol A",
            "permisos": [
                {
                    "id": 1
                },
                {
                    "id": 2
                }
            ]
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/roles/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        rol_db = Rol.objects.filter(Q(permisos__id=1) and Q(permisos__id=2) and Q(nombre=rol["nombre"]))
        self.assertEquals(len(rol_db), 1)
        self.assertEquals(rol_db[0].nombre, body["nombre"])
        self.assertEquals(rol_db[0].permisos.count(), len(body["permisos"]))

    def test_crear_rol_sin_agregar_permisos(self):
        """
        test_crear_rol_sin_agregar_permisos Prueba la creación de un rol de sistema sin permisos agregados
        """
        print("\nProbando crear un rol de sistema sin permisos agregados.")
        rol = {
            "nombre": "Rol X",
            "permisos": []
        }
        self.client.login(username="testing", password="polijira2021")
        roles_cant = Rol.objects.count()
        response = self.client.post("/api/roles/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["message"], "Debe tener al menos un permiso")
        rol_db = Rol.objects.filter(nombre=rol["nombre"])
        self.assertEquals(len(rol_db), 0)
        self.assertEquals(Rol.objects.count(), roles_cant)

    def test_crear_rol_con_permisos_inexistentes(self):
        """
        test_crear_rol_con_permisos_inexistentes Prueba la creación de un rol de sistema con permisos inexistentes
        """
        print("\nProbando crear un rol de sistema con permisos inexistentes.")
        rol = {
            "nombre": "Rol X",
            "permisos": [
                {
                    "id": 1
                },
                {
                    "id": 88
                }
            ]
        }
        self.client.login(username="testing", password="polijira2021")
        roles_cant = Rol.objects.count()
        response = self.client.post("/api/roles/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el permiso")
        rol_db = Rol.objects.filter(Q(permisos__id=1) and Q(permisos__id=88) and Q(nombre=rol["nombre"]))
        self.assertEquals(len(rol_db), 0)
        self.assertEquals(Rol.objects.count(), roles_cant)

    def test_eliminar_rol(self):
        """
        test_eliminar_rol Prueba la eliminación de un rol de sistema
        """
        print("\nProbando eliminar un rol de sistema.")
        self.client.login(username="testing", password="polijira2021")
        roles_cant = Rol.objects.count()
        response = self.client.delete("/api/roles/2/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["message"], "Rol Eliminado.")
        rol_db = Rol.objects.filter(pk=2)
        self.assertEquals(len(rol_db), 0)
        self.assertEquals(Rol.objects.count(), roles_cant - 1)

    def test_eliminar_rol_inexistente(self):
        """
        test_eliminar_rol_inexistente Prueba la eliminación de un rol de sistema inexistente
        """
        print("\nProbando eliminar un rol de sistema inexistente.")
        self.client.login(username="testing", password="polijira2021")
        roles_cant = Rol.objects.count()
        response = self.client.delete("/api/roles/99/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol")
        self.assertEquals(Rol.objects.count(), roles_cant)

    def test_modificar_rol(self):
        """
        test_modificar_rol Prueba la modificación de un rol de sistema
        """
        print("\nProbando modificar un rol de sistema.")
        rol = {
            "nombre": "Tirano"
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.put("/api/roles/1/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        rol_db = Rol.objects.filter(nombre=rol["nombre"], pk=1)
        self.assertEquals(len(rol_db), 1)
        self.assertEquals(rol_db[0].nombre, body["nombre"])

    def test_modificar_rol_inexistente(self):
        """
        test_modificar_rol_inexistente Prueba la modificación de un rol de sistema inexistente
        """
        print("\nProbando modificar un rol de sistema inexistente.")
        rol = {
            "nombre": "Dictador"
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.put("/api/roles/99/", rol, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol")

    def test_listar_permisos_de_rol(self):
        """
        test_listar_permisos_de_rol Prueba el listado de permisos de un rol de sistema
        """
        print("\nProbando listar permisos de un rol de sistema.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles/1/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(isinstance(body, list), True)
        rol = Rol.objects.get(pk=1)
        self.assertEquals(rol.permisos.count(), len(body))

    def test_listar_permisos_de_rol_inexistente(self):
        """
        test_listar_permisos_de_rol_inexistente Prueba el listado de permisos de un rol de sistema inexistente
        """
        print("\nProbando listar permisos de un rol de sistema inexistente.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/roles/99/permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol")

    def test_agregar_permiso_a_rol(self):
        """
        test_agregar_permiso_a_rol Prueba agregar un permiso a un rol de sistema
        """
        print("\nProbando agregar un permiso a un rol de sistema.")
        permiso = {
            "permiso_id": 2
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/roles/1/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        rol_db = Rol.objects.filter(permisos__id=permiso["permiso_id"], pk=1)
        self.assertEquals(len(rol_db), 1)
        self.assertEquals(rol_db[0].permisos.count(), len(body["permisos"]))

    def test_agregar_permiso_a_rol_inexistente(self):
        """
        test_agregar_permiso_a_rol_inexistente Prueba agregar un permiso a un rol de sistema inexistente
        """
        print("\nProbando agregar un permiso a un rol de sistema inexistente.")
        permiso = {
            "permiso_id": 2
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/roles/99/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol")

    def test_agregar_permiso_inexistente_a_rol(self):
        """
        test_agregar_permiso_inexistente_a_rol Prueba agregar un permiso inexistente a un rol de sistema
        """
        print("\nProbando agregar un permiso inexistente a un rol de sistema.")
        permiso = {
            "permiso_id": 88
        }
        self.client.login(username="testing", password="polijira2021")
        permisos_cant = Rol.objects.get(pk=1).permisos.count()
        response = self.client.post("/api/roles/1/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el permiso")
        rol = Rol.objects.get(pk=1)
        self.assertEquals(rol.permisos.count(), permisos_cant)

    def test_eliminar_permiso_a_rol(self):
        """
        test_eliminar_permiso_a_rol Prueba eliminar un permiso a un rol de sistema
        """
        print("\nProbando eliminar un permiso a un rol de sistema.")
        permiso = {
            "permiso_id": 1
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/roles/1/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        rol = Rol.objects.get(pk=1)
        self.assertEquals(rol.nombre, body["nombre"])
        self.assertEquals(rol.permisos.count(), len(body["permisos"]))

    def test_eliminar_permiso_a_rol_inexistente(self):
        """
        test_eliminar_permiso_a_rol_inexistente Prueba eliminar un permiso a un rol de sistema inexistente
        """
        print("\nProbando eliminar un permiso a un rol de sistema inexistente.")
        permiso = {
            "permiso_id": 2
        }
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/roles/99/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol")

    def test_eliminar_permiso_inexistente_a_rol(self):
        """
        test_eliminar_permiso_inexistente_a_rol Prueba eliminar un permiso inexistente a un rol de sistema
        """
        print("\nProbando eliminar un permiso inexistente a un rol de sistema.")
        permiso = {
            "permiso_id": 88
        }
        self.client.login(username="testing", password="polijira2021")
        permisos_cant = Rol.objects.get(pk=1).permisos.count()
        response = self.client.delete("/api/roles/1/permisos/", permiso, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el permiso")
        rol = Rol.objects.get(pk=1)
        self.assertEquals(rol.permisos.count(), permisos_cant)
