from django.http import response
from backend.api.models import Proyecto, Usuario
from django.test import TestCase, Client
from django.utils import timezone


class ProyectoTestCase(TestCase):
    """
    ProyectoTestCase Prueba las funcionalidades del modelo Proyecto
    """
    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
    ]

    def setUp(self):
        """
        setUp Configura el TestCase
        """
        self.client = Client()

    def test_listar_proyectos(self):
        """
        test_listar_proyectos Prueba el listado de todos los proyectos
        """
        print("\nProbando listar los proyectos.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/proyectos/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(isinstance(body, list), True)
        self.assertEquals(Proyecto.objects.count(), len(body))

    def test_listar_proyectos_sin_permiso(self):
        """
        test_listar_proyectos_sin_permiso Prueba el listado de todos los proyectos sin permiso
        """
        print("\nProbando listar los proyectos sin permiso")
        # rol = Usuario.objects.get(nombre="testing").rolP  #rolP asumiendo que ese seria el nombre del atributo de roles de proyecto en modelo Usuario
        # permiso = rol.permisos.get(codigo="ver_proyectos")
        # rol.eliminar_permiso(permiso)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/proyectos/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(isinstance(body, list), True)
        # self.assertEquals(Proyecto.object.filter(miembros__nombre="testing").count(), len(body))  #cant de proyectos del usuario y len(body) iguales

    def test_obtener_proyecto(self):
        """
        test_obtener_proyecto Prueba obtener los detalles de un proyecto
        """
        print("\nProbando obtener los detalles de un proyecto.")
        usuario = Usuario.objects.get(pk=2)
        proyecto = Proyecto.objects.create(
            nombre="ProyectoX", descripcion="Descripcion del proyecto X", fecha_inicio=timezone.now(), fecha_fin=timezone.now(), scrum_master=usuario)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/proyectos/"+str(proyecto.id)+"/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(proyecto.nombre, body["nombre"])

    def test_obtener_proyecto_no_propio_sin_permiso(self):
        """
        test_obtener_proyecto_no_propio_sin_permiso Prueba obtener los detalles de un proyecto no propio sin permiso
        """
        print("\nProbando obtener los detalles de un proyecto sin permiso.")
        # rol = Usuario.objects.get(nombre="testing").rolP  #rolP asumiendo que ese seria el nombre del atributo de roles de proyecto en modelo Usuario
        # permiso = rol.permisos.get(codigo="ver_proyectos")
        # rol.eliminar_permiso(permiso)
        usuario = Usuario.objects.get(pk=2)
        proyecto = Proyecto.objects.create(
            nombre="ProyectoX", descripcion="Descripcion del proyecto X", fecha_inicio=timezone.now(), fecha_fin=timezone.now(), scrum_master=usuario)
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/proyectos/"+str(proyecto.id)+"/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['ver_proyectos'])

    def test_crear_proyecto(self):
        """
        test_crear_proyecto Prueba la creación de un proyecto
        """
        print("\nProbando crear un proyecto.")
        proyecto = {
            "nombre": "Proyecto A",
            "descripcion": "Descripcion del proyecto",
            "scrum_master": 2
        }
        # no se si se debe pasar algun otro atributo de parametro en el body
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/proyectos/", proyecto, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        proyecto_db = Proyecto.objects.filter(nombre=proyecto["nombre"])
        self.assertEquals(len(proyecto_db), 1)
        self.assertEquals(proyecto_db[0].nombre, body["nombre"])

    def test_crear_proyecto_sin_permiso(self):
        """
        test_crear_proyecto_sin_permiso Prueba la creación de un proyecto sin permiso
        """
        print("\nProbando crear un proyecto sin permiso.")
        proyecto = {
            "nombre": "Proyecto A",
            "descripcion": "Descripcion del proyecto",
            "scrum_master": 2
        }
        # no se si se debe pasar algun otro atributo de parametro en el body
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/proyectos/", proyecto, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ['ver_usuarios', 'crear_proyectos'])
