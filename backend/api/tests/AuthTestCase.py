from backend.api.models.Usuario import Usuario
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
        self.assertEquals(response.status_code, 401)

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
        body = response.json()
        self.assertEquals(response.status_code, 401)
        self.assertEquals(body["error"], "unactivated")

    def test_wrong_start_path(self):
        """
        test_wrong_start_path Prueba si el path del request no inicia con /api
        """
        print("\nProbando obtener el path del request que no inicia con /api")
        response = self.c.get("/")
        response.json
        self.assertEquals(response.status_code, 200)

    def test_token_formato_incorrecto_sin_jwt(self):
        """
        test_token_formato_incorrecto_sin_jwt Prueba si el header tiene jwt
        """
        print("\nProbando enviar un formato sin JWT en el header")
        headers = {"HTTP_AUTHORIZATION": "fjdlajdkffd"}
        response = self.c.get("/api/usuarios/me/", **headers)
        self.assertEquals(response.status_code, 401)

    def test_token_formato_incorrecto_jwt(self):
        """
        test_token_formato_incorrecto_jwt Prueba si el jwt es correcto
        """
        print("\nProbando enviar un formato JWT incorrecto en el header")
        headers = {"HTTP_AUTHORIZATION": "JW " + self.get_token()}
        response = self.c.get("/api/usuarios/me/", **headers)
        self.assertEquals(response.status_code, 401)

    def test_usuario_nuevo_logueado(self):
        """
        test_usuario_nuevo_logueado Prueba si un usuario ingresa por primera vez en el sistema
        """
        print("\nProbando ingresar con un usuario nuevo al sistema")
        user = User.objects.get(username="testing")
        user.delete()
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.get_token()}
        response = self.c.get("/api/usuarios/me/", **headers)
        usuario = Usuario.objects.filter(
            user__first_name="Test PoliJira",
            user__email="test@polijira.com",
            nombre="Test PoliJira",
            email="test@polijira.com",
            estado="I",
            firebase_uid="A4rxPBjYBfQKrIUlElklVF2OTRI3"
        )
        body = response.json()
        self.assertEquals(body["error"], "unactivated")
        self.assertEquals(usuario.count(), 1)
        self.assertEquals(response.status_code, 401)

    def test_token_invalido(self):
        """
        test_token_invalido Prueba cuando el token enviado es invalido
        """
        print("\nProbando utilizar un token incorrecto")
        headers = {"HTTP_AUTHORIZATION": "JWT " + "fjdklsfjlskaf"}
        response = self.c.get("/api/usuarios/me/", **headers)
        self.assertEquals(response.status_code, 401)

    def test_token_expirado(self):
        """
        test_token_invalido Prueba cuando el token enviado esta expirado
        """
        print("\nProbando utilizar un token expirado")
        headers = {"HTTP_AUTHORIZATION": "JWT "
                   + "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM2NGU4NTQ1NzI5OWQ5NzIx"
                   + "YjczNDQyZGNiNTQ3Y2U2ZDk4NGRmNTkiLCJ0eXAiOiJKV1QifQ.ey"
                   + "JuYW1lIjoiU2ViYXMgQ2FuZSIsInBpY3R1cmUiOiJodHRwczovL2xo"
                   + "My5nb29nbGV1c2VyY29udGVudC5jb20vYS0vQU9oMTRHZ2F1TWJjM2"
                   + "9EZ284VUZQR1hCS1ExTXM0Y3hkV1R5b3oybG1QejY9czk2LWMiLCJp"
                   + "c3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcG9saW"
                   + "ppcmEtY2MxNDciLCJhdWQiOiJwb2xpamlyYS1jYzE0NyIsImF1dGhf"
                   + "dGltZSI6MTYyOTI2MTI0MCwidXNlcl9pZCI6ImV1WmZVS0g4enJhOE"
                   + "RMY1NYbkpPOHFlUjBhQzIiLCJzdWIiOiJldVpmVUtIOHpyYThETGNT"
                   + "WG5KTzhxZVIwYUMyIiwiaWF0IjoxNjI5MjYxMjQwLCJleHAiOjE2Mjk"
                   + "yNjQ4NDAsImVtYWlsIjoiY2FuZXNpMTJAZ21haWwuY29tIiwiZW1haW"
                   + "xfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiO"
                   + "nsiZ29vZ2xlLmNvbSI6WyIxMDM1NzAyMjEwMzE5NzgzMjg5MTIiXSwi"
                   + "ZW1haWwiOlsiY2FuZXNpMTJAZ21haWwuY29tIl19LCJzaWduX2luX3B"
                   + "yb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.iiRgqoCwMv9b70wiTesdzoT"
                   + "vm_QDou4pkkBsiTeI9wi6pY-xFhAWIIPE7AsNszI1YC_tUNn6SWLEUD"
                   + "9Pe-FLFfYiDyk2DKbzuCy45qGH3JHXVWLNbYjS56Ol_Jpx4MgRdIPBm"
                   + "73XWf6YyF-oPP4DJjzd-K_51Bmt1i0w5XgAiWq02f7hld2KXK8GERqx"
                   + "1P8pWTWlpBuwZGByJGZzmyxMgECz3WtvGPYoJt9GYZeMW-j5yqf4YUO"
                   + "DjRu7qFI4NEr8UjnBfaYVURGTR5cHt46sx9maGb8dlNkmW9xRTUhuNP"
                   + "cTFw968M3pmsO_AKkWkSwOGSRK9JrrcFIcaMNTxu4HHw"}
        response = self.c.get("/api/usuarios/me/", **headers)
        self.assertEquals(response.status_code, 401)
