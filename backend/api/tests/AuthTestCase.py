from backend.api.models.Usuario import Usuario
from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.contrib.auth.models import User
import pyrebase


class AuthTestCase(TestCase):
    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
    ]

    def setUp(self):
        self.c = Client()
        self.firebase = pyrebase.initialize_app(
            settings.FIREBASE_CLIENT_CONFIG)

    def getToken(self):
        auth = self.firebase.auth()
        u = auth.sign_in_with_email_and_password(
            settings.TESTING_USER_EMAIL, settings.TESTING_USER_PASSWORD)
        return u["idToken"]

    def test_login(self):
        print("\nProbando login de usuarios.")
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.getToken()}
        response = self.c.get("/api/usuarios/me/", **headers)
        self.assertEquals(response.status_code, 200)

    def test_me(self):
        print("\nProbando obtención perfil de usuario logueado.")
        self.c.login(username="testing", password="testing")
        response = self.c.get("/api/usuarios/me/")
        body = response.json()
        u = User.objects.get(username="testing")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["id"], u.usuario.id)

    def test_my_permissions(self):
        print("\nProbando obtención permisos de usuario logueado.")
        u = User.objects.get(username="testing")
        u.is_staff = False
        u.is_superuser = False
        u.save()
        self.c.login(username="testing", password="testing")
        response = self.c.get("/api/usuarios/mis_permisos/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(body), 12)

    def test_me_not_logged(self):
        print("\nProbando obtención de perfil de usuario sin loguearse.")
        response = self.c.get("/api/usuarios/me/")
        body = response.json()
        self.assertEquals(response.status_code, 403)

    def test_me_not_activated(self):
        print("\nProbando obtención perfil de usuario no activado.")
        u = User.objects.get(username="testing")
        usuario = u.usuario
        usuario.estado = "I"
        usuario.save()
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.getToken()}
        response = self.c.get("/api/usuarios/me/", **headers)
        body = response.json()
        self.assertEquals(response.status_code, 403)
