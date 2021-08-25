from backend.api.models.Usuario import Usuario
from django.test import TestCase
from django.test import Client


class UsuarioTestCase(TestCase):
    """
    UsuarioTestCase Prueba las funcionalidades del modelo Usuario
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
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
        print("\nProbando listar todos los usuarios")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.get("/api/usuarios/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(body), Usuario.objects.count())

    def test_obtener_usuario(self):
        """
        test_obtener_usuario Prueba obtener un usuario
        """
        print("\nProbando obtener un usuario")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.get("/api/usuarios/1/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body['id'], 1)

    def test_obtener_usuario_no_existente(self):
        """
        test_obtener_usuario_incorrecto Prueba obtener un usuario que no existe
        """
        print("\nProbando obtener un usuario que no existe")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.get("/api/usuarios/2/")
        self.assertEquals(response.status_code, 404)

    def test_activar_usuario(self):
        """
        test_activar_usuario Prueba activar un usuario
        """
        print("\nProbando activar un usuario")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.post("/api/usuarios/1/activar/")
        usuario = Usuario.objects.get(pk=1)
        self.assertEquals(usuario.estado, "A")
        self.assertEquals(response.status_code, 200)

    def test_activar_usuario_no_existente(self):
        """
        test_activar_usuario Prueba activar un usuario no existente
        """
        print("\nProbando activar un usuario que no existe")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.post("/api/usuarios/2/activar/")
        self.assertEquals(response.status_code, 404)

    def test_desactivar_usuario(self):
        """
        test_desactivar_usuario Prueba desactivar un usuario
        """
        print("\nProbando desactivar un usuario")
        self._client.login(username="testing", password="polijira2021")
        usuario = Usuario.objects.create(
            email="uncorreo@correo.com",
            estado="A"
        )
        response = self._client.post("/api/usuarios/"+str(usuario.id)+"/desactivar/")
        usuario = Usuario.objects.get(pk=usuario.id)
        self.assertEquals(usuario.estado, "I")
        self.assertEquals(response.status_code, 200)

    def test_desactivar_el_mismo_usuario(self):
        """
        test_desactivar_usuario Prueba desactivar un usuario a si mismo
        """
        print("\nProbando desactivar un usuario a si mismo")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.post("/api/usuarios/1/desactivar/")
        self.assertEquals(response.status_code, 409)

    def test_desactivar_usuario_no_existente(self):
        """
        test_desactivar_usuario_no_existente Prueba desactivar un usuario que no existe
        """
        print("\nProbando desactivar un usuario que no existe")
        self._client.login(username="testing", password="polijira2021")
        response = self._client.post("/api/usuarios/2/desactivar/")
        self.assertEquals(response.status_code, 404)
