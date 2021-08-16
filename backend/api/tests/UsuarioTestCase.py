from backend.api.models.Usuario import Usuario
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings
import firebase_admin
from firebase_admin import credentials


class UsuarioTestCase(APITestCase):

    def test_crear_usuario(self):
        """Asegura que podemos crear un nuevo usuario
        """
        print("\nObteniendo credenciales de firebase")
        cred = credentials.Certificate(settings.FIREBASE_CONFIG)
        firebase_admin.get_app(cred)
        url = reverse('usuarios')
        data = {'nombre': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(Usuario.objects.get().nombre, 'test')
        print("\nOK")
        print("\nIntentado loguear")
