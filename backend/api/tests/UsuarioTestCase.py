from backend.api.models.Usuario import Usuario
from backend.api.models import Permiso
from django.test import TestCase
from django.test import Client


class UsuarioTestCase(TestCase):
    """
    UsuarioTestCase Prueba las funcionalidades del modelo Usuario
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
        "backend/api/fixtures/testing/permisos.json",
        "backend/api/fixtures/testing/roles.json"
    ]

    def setUp(self):
        """
        setUp Configura el TestCase
        """
        self._client = Client()

    def test_listar_usuario(self):
        """
        test_listar_usuario Prueba listar todos los usuarios
        """
        print("\nProbando listar todos los usuarios.")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.get("/api/usuarios/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(body), Usuario.objects.count())

    def test_listar_usuario_sin_permiso(self):
        """
        test_listar_usuario_sin_permiso Prueba listar todos los usuarios sin permiso
        """
        print("\nProbando listar todos los usuarios sin permiso.")
        rol = Usuario.objects.get(nombre="testing").rol
        permiso = rol.permisos.get(codigo="ver_usuarios")
        rol.eliminar_permiso(permiso)
        self._client.login(username="testing", password="polijira2021")
        response = self._client.get("/api/usuarios/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['ver_usuarios'])

    def test_obtener_usuario(self):
        """
        test_obtener_usuario Prueba obtener un usuario
        """
        print("\nProbando obtener un usuario.")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.get("/api/usuarios/2/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body['id'], 2)

    def test_obtener_usuario_sin_permiso(self):
        """
        test_obtener_usuario_sin_permiso Prueba obtener un usuario sin permiso
        """
        print("\nProbando obtener un usuario sin permiso.")
        rol = Usuario.objects.get(nombre="testing").rol
        permiso = rol.permisos.get(codigo="ver_usuarios")
        rol.eliminar_permiso(permiso)
        self._client.login(username="testing", password="polijira2021")
        response = self._client.get("/api/usuarios/2/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['ver_usuarios'])

    def test_obtener_usuario_no_existente(self):
        """
        test_obtener_usuario_incorrecto Prueba obtener un usuario que no existe
        """
        print("\nProbando obtener un usuario que no existe.")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.get("/api/usuarios/33/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el usuario")

    def test_activar_usuario(self):
        """
        test_activar_usuario Prueba activar un usuario
        """
        print("\nProbando activar un usuario.")
        self._client.login(username="testing", password="polijira2021")
        Usuario.objects.get(pk=2).estado = 'I'
        response = self._client.post("/api/usuarios/2/activar/")
        usuario_db = Usuario.objects.get(pk=2)
        self.assertEquals(usuario_db.estado, "A")
        self.assertEquals(response.status_code, 200)

    def test_activar_usuario_sin_permiso(self):
        """
        test_activar_usuario_sin_permiso Prueba activar un usuario sin permiso
        """
        print("\nProbando activar un usuario sin permiso.")
        rol = Usuario.objects.get(nombre="testing").rol
        permiso = rol.permisos.get(codigo="activar_usuarios")
        rol.eliminar_permiso(permiso)
        usuario = Usuario.objects.get(pk=2)
        usuario.estado = 'I'
        self._client.login(username="testing", password="polijira2021")
        response = self._client.post("/api/usuarios/2/activar/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['activar_usuarios'])
        self.assertEquals(usuario.estado, "I")

    def test_activar_usuario_no_existente(self):
        """
        test_activar_usuario Prueba activar un usuario no existente
        """
        print("\nProbando activar un usuario que no existe.")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.post("/api/usuarios/33/activar/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el usuario")

    def test_desactivar_usuario(self):
        """
        test_desactivar_usuario Prueba desactivar un usuario
        """
        print("\nProbando desactivar un usuario.")
        self._client.login(username="testing", password="polijira2021")
        usuario = Usuario.objects.create(
            email="uncorreo@correo.com",
            estado="A"
        )
        response = self._client.post("/api/usuarios/"+str(usuario.id)+"/desactivar/")
        usuario = Usuario.objects.get(pk=usuario.id)
        self.assertEquals(usuario.estado, "I")
        self.assertEquals(response.status_code, 200)

    def test_desactivar_usuario_sin_permiso(self):
        """
        test_desactivar_usuario_sin_permiso Prueba desactivar un usuario sin permiso
        """
        print("\nProbando desactivar un usuario sin permiso.")
        rol = Usuario.objects.get(nombre="testing").rol
        permiso = rol.permisos.get(codigo="desactivar_usuarios")
        rol.eliminar_permiso(permiso)
        Usuario.objects.get(pk=2).estado = 'A'
        self._client.login(username="testing", password="polijira2021")
        response = self._client.post("/api/usuarios/2/desactivar/")
        body = response.json()
        usuario_db = Usuario.objects.get(pk=2)
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['desactivar_usuarios'])
        self.assertEquals(usuario_db.estado, "A")

    def test_desactivar_el_mismo_usuario(self):
        """
        test_desactivar_usuario Prueba desactivar un usuario a si mismo
        """
        print("\nProbando desactivar un usuario a si mismo.")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.post("/api/usuarios/1/desactivar/")
        body = response.json()
        self.assertEquals(response.status_code, 409)
        self.assertEquals(body["message"], "No puedes desactivarte a ti mismo")

    def test_desactivar_usuario_no_existente(self):
        """
        test_desactivar_usuario_no_existente Prueba desactivar un usuario que no existe
        """
        print("\nProbando desactivar un usuario que no existe.")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.post("/api/usuarios/33/desactivar/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el usuario")

    def test_asignar_rol(self):
        """
        test_asignar_rol Prueba asignar un rol a un usuario
        """
        print("\nProbando asignar rol a un usuario.")
        self._client.login(username="testing", password="polijira2021")
        body = {
            "id": 1
        }
        response = self._client.post("/api/usuarios/2/asignar_rol/", body)
        usuario = Usuario.objects.get(pk=2)
        rol = usuario.rol
        self.assertEquals(response.status_code, 200)
        self.assertEquals(rol.id, 1)

    def test_asignar_rol_sin_permiso(self):
        """
        test_asignar_rol_sin_permiso Prueba asignar un rol a un usuario sin tener permiso para asignar roles
        """
        print("\nProbando asignar rol sin permisos.")
        self._client.login(username="testing", password="polijira2021")
        rol = Usuario.objects.get(nombre="testing").rol
        permiso = Permiso.objects.get(codigo="asignar_roles")
        rol.eliminar_permiso(permiso)
        body = {
            "id": 2
        }
        response = self._client.post("/api/usuarios/2/asignar_rol/", body)
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_usuarios", "ver_roles", "asignar_roles"])

    def test_asignar_rol_a_si_mismo(self):
        """
        test_asignar_rol_a_si_mismo Prueba asignar un rol a sí mismo
        """
        print("\nProbando asignar un rol a sí mismo.")
        self._client.login(username="testing", password="polijira2021")
        rol = {
            "id": 1
        }
        usuario = Usuario.objects.get(nombre="testing")
        response = self._client.post("/api/usuarios/"+str(usuario.id)+"/asignar_rol/", rol)
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No puede asignarse roles a sí mismo")

    def test_asignar_rol_no_existente(self):
        """
        test_asignar_rol_no_existente Prueba asignar un rol que no existe a un usuario
        """
        print("\nProbando asignar un rol que no existe.")
        self._client.login(username="testing", password="polijira2021")
        body = {
            "id": 33
        }
        response = self._client.post("/api/usuarios/2/asignar_rol/", body)
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el rol")

    def test_asignar_rol_a_usuario_inexistente(self):
        """
        test_asignar_rol_a_usuario_inexistente Prueba asignar un rol a un usuario que no existe
        """
        print("\nProbando asignar rol a un usuario que no existe.")
        self._client.login(username="testing", password="polijira2021")
        body = {
            "id": 1
        }
        response = self._client.post("/api/usuarios/33/asignar_rol/", body)
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEquals(body["message"], "No existe el usuario")
