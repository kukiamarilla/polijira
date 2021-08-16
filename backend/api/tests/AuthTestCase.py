from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.contrib.auth.models import User
import requests


class AuthTestCase(TestCase):
    """
    AuthTestCase Prueba las funcionalidades de autenticacion del sistema
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
    ]

    def setUp(self):
        """
        setUp Configura el testcase
        """
        self.c = Client()

    def get_token(self):
        """
        get_token Consigue el id token del usuario de prueba de firebase

        Returns:
            str: Retorna el idToken
        """
        api_key = settings.FIREBASE_CLIENT_CONFIG["apiKey"]
        url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + api_key
        data = {
            "email": settings.TESTING_USER_EMAIL,
            "password": settings.TESTING_USER_PASSWORD,
            "returnSecureToken": True
        }
        response = requests.post(url, data=data).json()
        return response['idToken']

    def test_login(self):
        """
        test_login Prueba la autenticación exitosa
        """
        print("\nProbando login de usuarios.")
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.get_token()}
        response = self.c.get("/api/usuarios/me/", **headers)
        self.assertEquals(response.status_code, 200)

    def test_me(self):
        """
        test_me Prueba si el usuario puede acceder a su perfil
        """
        print("\nProbando obtención perfil de usuario logueado.")
        self.c.login(username="testing", password="polijira2021")
        response = self.c.get("/api/usuarios/me/")
        body = response.json()
        u = User.objects.get(username="testing")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["id"], u.usuario.id)

    def test_me_not_logged(self):
        """
        test_me_not_logged Prueba la denegación de acceso de los usuario no logueados
        """
        print("\nProbando obtención de perfil de usuario sin loguearse.")
        response = self.c.get("/api/usuarios/me/")
        response.json()
        self.assertEquals(response.status_code, 403)

    def test_me_not_activated(self):
        """
        test_me_not_activated Prueba la denegación de acceso de los usuarios no activados
        """
        print("\nProbando obtención perfil de usuario no activado.")
        u = User.objects.get(username="testing")
        usuario = u.usuario
        usuario.estado = "I"
        usuario.save()
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.get_token()}
        response = self.c.get("/api/usuarios/me/", **headers)
        response.json()
        self.assertEquals(response.status_code, 403)
