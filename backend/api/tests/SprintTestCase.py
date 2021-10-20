from datetime import date, timedelta
from django.test import TestCase, Client
from rest_framework import response
from backend.api.models import Sprint, Miembro, PermisoProyecto
from backend.api.models.SprintBacklog import SprintBacklog
from backend.api.serializers import SprintSerializer


class SprintTestCase(TestCase):
    """
    SprintTestCase Prueba las funcionalidades de un Sprint

    Args:
        TestCase (TestCase): Modelo Test del módulo django
    """

    fixtures = [
        "backend/api/fixtures/testing/auth.json",
        "backend/api/fixtures/testing/usuarios.json",
        "backend/api/fixtures/testing/permisos.json",
        "backend/api/fixtures/testing/roles.json",
        "backend/api/fixtures/testing/proyectos.json",
        "backend/api/fixtures/testing/permisosProyecto.json",
        "backend/api/fixtures/testing/plantillas.json",
        "backend/api/fixtures/testing/rolesProyecto.json",
        "backend/api/fixtures/testing/miembros.json",
        "backend/api/fixtures/testing/horarios.json",
        "backend/api/fixtures/testing/user-stories.json",
        "backend/api/fixtures/testing/product-backlogs.json",
        "backend/api/fixtures/testing/registro-user-stories.json",
        "backend/api/fixtures/testing/sprints.json",
        "backend/api/fixtures/testing/sprintbacklogs.json",
        "backend/api/fixtures/testing/miembrosprints.json"
    ]

    def setUp(self):
        """
        setUp Configura el TestCase
        """
        self.client = Client()

    def test_desactivar_usuario_en_sprint_activo(self):
        """
        test_desactivar_usuario_en_sprint_activo Prueba desactivar un Usuario que pertenece a un Sprint activo
        """
        print("\nProbando desactivar un usuario que pertenece a un Sprint Activo")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.post("/api/usuarios/2/desactivar/")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_obtener_sprint(self):
        """
        test_obtener_sprint Prueba obtener los detalles de un Sprint
        """
        print("\nProbando obtener los detalles de un Sprint")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/sprints/1/")
        self.assertEquals(response.status_code, 200)
        sprint = Sprint.objects.get(pk=1)
        sprint_serializer = SprintSerializer(sprint, many=False)
        body = response.json()
        self.assertDictEqual(body, sprint_serializer.data)

    def test_obtener_sprint_sin_permiso_ver_sprints(self):
        """
        test_obtener_sprint_sin_permiso_ver_sprints
        Prueba obtener los detalles de un Sprint sin tener el permiso de proyecto: Ver Sprints
        """
        print("\nProbando obtener los detalles de un Sprint sin tener el permiso de proyecto: Ver Sprints")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_sprints").delete()
        response = self.client.get("/api/sprints/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_sprints"])
        self.assertEquals(body["error"], "forbidden")

    def test_obtener_sprint_no_existente(self):
        """
        test_obtener_sprint_no_existente Prueba obtener los detalles de un Sprint que no existe
        """
        print("\nProbando obtener los detalles de un Sprint que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/sprints/1000/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_obtener_sprint_sin_ser_miembro(self):
        """
        test_obtener_sprint_sin_ser_miembro Prueba obtener los detalles de un Sprint sin ser miembro del Proyecto
        """
        print("\nProbando obtener los detalles de un Sprint sin ser miembro del Proyecto")
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.get(pk=4)
        miembro.usuario_id = 2
        miembro.save()
        response = self.client.get("/api/sprints/1/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_crear_sprint(self):
        """
        test_crear_sprint Prueba crear un Sprint
        """
        print("\nProbando crear un Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": str(date.today()),
            "fecha_fin": str(date.today() + timedelta(5)),
            "proyecto": 3
        }
        sprints = Sprint.objects.all()
        for sprint in sprints:
            sprint.delete()
        response = self.client.post("/api/sprints/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        body.pop("id")
        sprint = {
            "numero": Sprint.objects.filter(proyecto_id=3).count(),
            "fecha_inicio": request_data.get("fecha_inicio"),
            "fecha_fin": request_data.get("fecha_fin"),
            "estado": "P",
            "estado_sprint_planning": "P",
            "planificador": None,
            "proyecto": 3
        }
        self.assertDictEqual(body, sprint)
        sprintBD = Sprint.objects.filter(**body)
        self.assertEquals(len(sprintBD), 1)

    def test_crear_sprint_sin_ser_miembro(self):
        """
        test_crear_sprint_sin_ser_miembro Prueba crear un Sprint sin ser miembro del Proyecto
        """
        print("\nProbando crear un Sprint sin ser miembro del Proyecto")
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.get(pk=4)
        miembro.usuario_id = 2
        miembro.save()
        request_data = {
            "fecha_inicio": str(date.today()),
            "fecha_fin": str(date.today() + timedelta(5)),
            "capacidad": 30,
            "proyecto": 3
        }
        response = self.client.post("/api/sprints/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_crear_sprint_sin_permiso_crear_sprints(self):
        """
        test_crear_sprint_sin_permiso_crear_sprints
        Prueba crear un Sprint sin tener permiso de proyecto: Crear Sprints
        """
        print("\nProbando crear un Sprint sin tener permiso: Crear Sprints")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="crear_sprints").delete()
        request_data = {
            "fecha_inicio": str(date.today()),
            "fecha_fin": str(date.today() + timedelta(5)),
            "capacidad": 30,
            "proyecto": 3
        }
        response = self.client.post("/api/sprints/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")
        self.assertEquals(body["permission_required"], ["crear_sprints"])

    def test_crear_sprint_fecha_solapada_1(self):
        """
        test_crear_sprint_fecha_solapada_1
        Prueba crear un Sprint pasando una fecha que se encuentra dentro del intervalo de otro Sprint
        """
        print("\nProbando crear un Sprint con una fecha que se encuentra dentro del intervalo de otro Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": "2022-11-05",
            "fecha_fin": "2022-11-23",
            "capacidad": 30,
            "proyecto": 3
        }
        response = self.client.post("/api/sprints/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_crear_sprint_fecha_solapada_2(self):
        """
        test_crear_sprint_fecha_solapada_2
        Prueba crear un Sprint pasando una fecha que se encuentra en el intervalo de otro Sprint 1
        """
        print("\nProbando crear un Sprint con una fecha que se encuentra en el intervalo de otro Sprint 1")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": "2022-11-03",
            "fecha_fin": "2022-11-24",
            "capacidad": 30,
            "proyecto": 3
        }
        response = self.client.post("/api/sprints/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_crear_sprint_fecha_solapada_3(self):
        """
        test_crear_sprint_fecha_solapada_3
        Prueba crear un Sprint pasando una fecha que se encuentra en el intervalo de otro Sprint 2
        """
        print("\nProbando crear un Sprint con una fecha que se encuentra en el intervalo de otro Sprint 2")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": "2022-11-08",
            "fecha_fin": "2022-11-24",
            "capacidad": 30,
            "proyecto": 3
        }
        response = self.client.post("/api/sprints/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_crear_sprint_fecha_solapada_4(self):
        """
        test_crear_sprint_fecha_solapada_4
        Prueba crear un Sprint pasando una fecha que se encuentra en el mismo intervalo de otro Sprint
        """
        print("\nProbando crear un Sprint con una fecha que se encuentra en el mismo intervalo de otro Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": "2022-11-04",
            "fecha_fin": "2022-11-24",
            "capacidad": 30,
            "proyecto": 3
        }
        response = self.client.post("/api/sprints/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_validar_crear_sprint_all(self):
        """
        test_validar_crear_sprint_all Prueba validar los datos enviados al crear un Sprint
        """
        print("\nProbando validar: Creacion de Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": "2021-09-01",
            "fecha_fin": "2021-09-10",
            "proyecto": 1000
        }
        response = self.client.post("/api/sprints/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        errors = response.json().get("errors")
        self.assertEquals(len(errors["fecha_inicio"]), 1)
        self.assertEquals(len(errors["proyecto"]), 1)

    def test_validar_crear_sprint_fecha_fin(self):
        """
        test_validar_crear_sprint_fecha_fin Valida si la fecha de fin es mayor a la fecha de inicio al Crear un Sprint
        """
        print("\nProbando validar: La fecha de fin al Crear un Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() - timedelta(5),
            "capacidad": 30,
            "proyecto": 1
        }
        response = self.client.post("/api/sprints/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        errors = response.json().get("errors")
        self.assertEquals(len(errors["fecha_fin"]), 1)

    def test_validar_crear_sprint_proyecto(self):
        """
        test_validar_crear_sprint_proyecto Prueba validar que el proyecto esté activado al Crear un Sprint
        """
        print("\nProbando validar: El estado del Proyecto al Crear Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() + timedelta(5),
            "capacidad": 30,
            "proyecto": 1
        }
        response = self.client.post("/api/sprints/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        errors = response.json().get("errors")
        self.assertEquals(len(errors["proyecto"]), 1)

    def test_modificar_sprint(self):
        """
        test_modificar_sprint Prueba modificar un Sprint
        """
        print("\nProbando modificar un Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() + timedelta(5)
        }
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        sprint = Sprint.objects.filter(**body)[0]
        self.assertEquals(sprint.fecha_inicio, request_data.get("fecha_inicio"))
        self.assertEquals(sprint.fecha_fin, request_data.get("fecha_fin"))

    def test_modificar_sprint_no_existente(self):
        """
        test_modificar_sprint_no_existente Prueba modificar los detalles de un Sprint que no existe
        """
        print("\nProbando modificar un Sprint que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() + timedelta(5),
            "capacidad": 30,
            "proyecto": 1
        }
        response = self.client.put("/api/sprints/1000/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_modificar_sprint_sin_ser_miembro(self):
        """
        test_modificar_sprint_sin_ser_miembro Prueba modificar un Sprint sin ser miembro del Proyecto
        """
        print("\nProbando modificar un Sprint sin ser miembro del Proyecto")
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.get(pk=4)
        miembro.usuario_id = 2
        miembro.save()
        request_data = {
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() + timedelta(5)
        }
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_sprint_sin_permiso_ver_sprints(self):
        """
        test_modificar_sprint_sin_permiso_ver_sprints
        Prueba modificar un Sprint sin tener el permiso de proyecto: Ver Sprints
        """
        print("\nProbando modificar un Sprint sin tener el permiso de proyecto: Ver Sprints")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_sprints").delete()
        request_data = {
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() + timedelta(5),
            "capacidad": 30,
            "proyecto": 1
        }
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_sprints", "modificar_sprints"])
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_sprint_sin_permiso_modificar_sprints(self):
        """
        test_modificar_sprint_sin_permiso_modificar_sprints
        Prueba modificar un Sprint sin tener el permiso de proyecto: modificar Sprints
        """
        print("\nProbando modificar un Sprint sin tener el permiso de proyecto: Modificar Sprints")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="modificar_sprints").delete()
        request_data = {
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() + timedelta(5),
            "capacidad": 30,
            "proyecto": 1
        }
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_sprints", "modificar_sprints"])
        self.assertEquals(body["error"], "forbidden")

    def test_modificar_sprint_activo(self):
        """
        test_modificar_sprint_activo Prueba modificar un Sprint en estado Activo
        """
        print("\nProbando modificar un Sprint en estado Activo")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() + timedelta(5),
            "capacidad": 30,
            "proyecto": 1
        }
        sprint = Sprint.objects.get(pk=2)
        sprint.activar()
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_modificar_sprint_finalizado(self):
        """
        test_modificar_sprint_finalizado Prueba modificar un Sprint en estado Finalizado
        """
        print("\nProbando modificar un Sprint en estado Finalizado")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() + timedelta(5),
            "capacidad": 30,
            "proyecto": 1
        }
        sprint = Sprint.objects.get(pk=2)
        sprint.finalizar()
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_modificar_sprint_fecha_solapada_1(self):
        """
        test_modificar_sprint_fecha_solapada_1
        Prueba modificar un Sprint pasando una fecha que se encuentra dentro del intervalo de otro Sprint
        """
        print("\nProbando modificar un Sprint con una fecha que se encuentra dentro del intervalo de otro Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": "2022-11-05",
            "fecha_fin": "2022-11-23",
            "capacidad": 30,
            "proyecto": 1
        }
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_modificar_sprint_fecha_solapada_2(self):
        """
        test_modificar_sprint_fecha_solapada_2
        Prueba modificar un Sprint pasando una fecha que se encuentra en el intervalo de otro Sprint 1
        """
        print("\nProbando modificar un Sprint con una fecha que se encuentra en el intervalo de otro Sprint 1")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": "2022-11-03",
            "fecha_fin": "2022-11-24",
            "capacidad": 30,
            "proyecto": 1
        }
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_modificar_sprint_fecha_solapada_3(self):
        """
        test_modificar_sprint_fecha_solapada_3
        Prueba modificar un Sprint pasando una fecha que se encuentra en el intervalo de otro Sprint 2
        """
        print("\nProbando modificar un Sprint con una fecha que se encuentra en el intervalo de otro Sprint 2")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": "2022-11-08",
            "fecha_fin": "2022-11-24",
            "capacidad": 30,
            "proyecto": 1
        }
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_modificar_sprint_fecha_solapada_4(self):
        """
        test_modificar_sprint_fecha_solapada_4
        Prueba modificar un Sprint pasando una fecha que se encuentra en el mismo intervalo de otro Sprint
        """
        print("\nProbando modificar un Sprint con una fecha que se encuentra en el mismo intervalo de otro Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": "2022-11-04",
            "fecha_fin": "2022-11-24",
            "capacidad": 30,
            "proyecto": 1
        }
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_validar_modificar_sprint_fecha_fin(self):
        """
        test_validar_modificar_sprint_fecha_fin Valida si la fecha
        de fin es mayor a la fecha de inicio al Modificar un Sprint
        """
        print("\nProbando validar: La fecha de fin al Modificar un Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": date.today(),
            "fecha_fin": date.today() - timedelta(5)
        }
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        errors = response.json().get("errors")
        self.assertEquals(len(errors["fecha_fin"]), 1)

    def test_validar_modificar_sprint_fecha_inicio(self):
        """
        test_validar_modificar_sprint_fecha_fin Valida si la fecha de inicio
        no esté en el pasado al Modificar un Sprint
        """
        print("\nProbando validar: La fecha de inicio al Modificar un Sprint")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "fecha_inicio": date.today() - timedelta(5),
            "fecha_fin": date.today()
        }
        response = self.client.put("/api/sprints/2/", request_data, content_type="application/json")
        self.assertEquals(response.status_code, 422)
        errors = response.json().get("errors")
        self.assertEquals(len(errors["fecha_inicio"]), 1)

    def test_eliminar_sprint(self):
        """
        test_eliminar_sprint Prueba eliminar un Sprint
        """
        print("\nProbando eliminar un Sprint")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/sprints/2/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        self.assertEquals(body["message"], "Sprint Eliminado")
        sprint = Sprint.objects.filter(pk=2)
        self.assertEquals(len(sprint), 0)

    def test_eliminar_sprint_no_existente(self):
        """
        test_eliminar_sprint_no_existente Prueba eliminar un Sprint que no existe en la BD
        """
        print("\nProbando eliminar un Sprint que no existe")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/sprints/1000/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_eliminar_sprint_sin_ser_miembro(self):
        """
        test_eliminar_sprint_sin_ser_miembro Prueba eliminar un Sprint sin ser miembro del Proyecto
        """
        print("\nProbando eliminar un Sprint sin ser miembro del Proyecto")
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.get(pk=4)
        miembro.usuario_id = 2
        miembro.save()
        response = self.client.delete("/api/sprints/2/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_eliminar_sprint_sin_permiso_ver_sprints(self):
        """
        test_eliminar_sprint_sin_permiso_ver_sprints
        Prueba elimina un Sprint sin tener el permiso de proyecto: Ver Sprints
        """
        print("\nProbando eliminar un Sprint sin tener el permiso de proyecto: Ver Sprints")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_sprints").delete()
        response = self.client.delete("/api/sprints/2/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_sprints", "eliminar_sprints"])
        self.assertEquals(body["error"], "forbidden")

    def test_eliminar_sprint_sin_permiso_eliminar_sprints(self):
        """
        test_eliminar_sprint_sin_permiso_eliminar_sprints
        Prueba elimina un Sprint sin tener el permiso de proyecto: Eliminar Sprints
        """
        print("\nProbando eliminar un Sprint sin tener el permiso de proyecto: Eliminar Sprints")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="eliminar_sprints").delete()
        response = self.client.delete("/api/sprints/2/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["permission_required"], ["ver_sprints", "eliminar_sprints"])
        self.assertEquals(body["error"], "forbidden")

    def test_eliminar_sprint_activo(self):
        """
        test_eliminar_sprint_activo Prueba eliminar un Sprint Activo
        """
        print("\nProbando eliminar un Sprint Activo")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/sprints/1/")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_eliminar_sprint_finalizado(self):
        """
        test_eliminar_sprint_finalizado Prueba eliminar un Sprint Finalizado
        """
        print("\nProbando eliminar un Sprint Finalizado")
        self.client.login(username="testing", password="polijira2021")
        sprint = Sprint.objects.get(pk=1)
        sprint.finalizar()
        response = self.client.delete("/api/sprints/1/")
        self.assertEquals(response.status_code, 409)
        body = response.json()
        self.assertEquals(body["error"], "conflict")

    def test_listar_sprint_backlogs(self):
        """
        test_listar_sprint_backlogs Prueba listar los sprint backlogs de un Sprint
        """
        print("\nProbando listar los sprint backlogs de un Sprint")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/sprints/1/sprint_backlogs/")
        self.assertEquals(response.status_code, 200)
        body = response.json()
        sprint = Sprint.objects.get(pk=1)
        self.assertEquals(len(body), sprint.sprint_backlogs.count())

    def test_listar_sprint_backlogs_no_existente(self):
        """
        test_listar_sprint_backlogs_no_existente Prueba listar los sprint backlogs de un Sprint que no existe en la BD
        """
        print("\nProbando listar los sprint backlogs de un Sprint que no existe en la BD")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/sprints/1000/sprint_backlogs/")
        self.assertEquals(response.status_code, 404)
        body = response.json()
        self.assertEquals(body["error"], "not_found")

    def test_listar_sprint_backlogs_sin_ser_miembro(self):
        """
        test_listar_sprint_backlogs_sin_ser_miembro Prueba listar los sprint
        backlogs de un Sprint  sin ser miembro del Proyecto
        """
        print("\nProbando listar los sprint backlogs de un Sprint sin ser miembro del Proyecto")
        self.client.login(username="testing", password="polijira2021")
        miembro = Miembro.objects.get(pk=4)
        miembro.usuario_id = 2
        miembro.save()
        response = self.client.get("/api/sprints/1/sprint_backlogs/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_listar_sprint_backlogs_sin_permiso_ver_sprints(self):
        """
        test_listar_sprint_backlogs_sin_permiso_ver_sprints
        Prueba listar los sprint backlogs de un Sprint sin tener permiso de Proyecto: Ver Sprints
        """
        print("\nProbando listar los sprint backlogs de un Sprint sin tener permiso de Proyecto: Ver Sprints")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_sprints").delete()
        response = self.client.get("/api/sprints/1/sprint_backlogs/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_listar_sprint_backlogs_sin_permiso_ver_user_stories(self):
        """
        test_listar_sprint_backlogs_sin_permiso_ver_user_stories
        Prueba listar los sprint backlogs de un Sprint sin tener permiso de Proyecto: Ver User Stories
        """
        print("\nProbando listar los sprint backlogs de un Sprint sin tener permiso de Proyecto: Ver User Stories")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        response = self.client.get("/api/sprints/1/sprint_backlogs/")
        self.assertEquals(response.status_code, 403)
        body = response.json()
        self.assertEquals(body["error"], "forbidden")

    def test_mover_kanban(self):
        """
        test_mover_kanban Prueba mover un user story a otra columna del kanban
        """
        print("\nProbando mover un user story a otra columna del kanban.")
        self.client.login(username="testing", password="polijira2021")
        sprint = Sprint.objects.get(pk=1)
        request_data = {
            "user_story": 1,
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprints/" + str(sprint.pk) + "/mover_kanban/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(body["sprint"]["id"], sprint.pk)
        self.assertEquals(body["user_story"]["id"], request_data["user_story"])
        self.assertEquals(body["estado_kanban"], request_data["estado_kanban"])

    def test_mover_kanban_sin_permiso_ver_kanban(self):
        """
        test_mover_kanban_sin_permiso_ver_kanban Prueba mover un user story a otra columna del kanban sin permiso ver kanban
        """
        print("\nProbando mover un user story a otra columna del kanban sin permiso ver kanban.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_kanban").delete()
        sprint = Sprint.objects.get(pk=1)
        request_data = {
            "user_story": 1,
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprints/" + str(sprint.pk) + "/mover_kanban/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_kanban", "ver_user_stories", "mover_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_mover_kanban_sin_permiso_ver_user_stories(self):
        """
        test_mover_kanban_sin_permiso_ver_user_stories Prueba mover un user story a otra columna del kanban sin permiso ver user stories
        """
        print("\nProbando mover un user story a otra columna del kanban sin permiso ver user stories.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        sprint = Sprint.objects.get(pk=1)
        request_data = {
            "user_story": 1,
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprints/" + str(sprint.pk) + "/mover_kanban/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_kanban", "ver_user_stories", "mover_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_mover_kanban_sin_permiso_mover_user_stories(self):
        """
        test_mover_kanban_sin_permiso_mover_user_stories Prueba mover un user story a otra columna del kanban sin permiso mover user stories
        """
        print("\nProbando mover un user story a otra columna del kanban sin permiso mover user stories.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="mover_user_stories").delete()
        sprint = Sprint.objects.get(pk=1)
        request_data = {
            "user_story": 1,
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprints/" + str(sprint.pk) + "/mover_kanban/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEquals(body["permission_required"], ["ver_kanban", "ver_user_stories", "mover_user_stories"])
        self.assertEquals(body["error"], "forbidden")

    def test_mover_kanban_con_user_story_sin_especificar(self):
        """
        test_mover_kanban_con_user_story_sin_especificar Prueba mover un user story a otra columna del kanban con user story sin especificar
        """
        print("\nProbando mover un user story a otra columna del kanban con user story sin especificar.")
        self.client.login(username="testing", password="polijira2021")
        sprint = Sprint.objects.get(pk=1)
        request_data = {
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprints/" + str(sprint.pk) + "/mover_kanban/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["user_story"], ["No especificaste el user story"])

    def test_mover_kanban_con_user_story_inexistente(self):
        """
        test_mover_kanban_con_user_story_inexistente Prueba mover un user story a otra columna del kanban con user story inexistente
        """
        print("\nProbando mover un user story a otra columna del kanban con user story inexistente.")
        self.client.login(username="testing", password="polijira2021")
        sprint = Sprint.objects.get(pk=1)
        request_data = {
            "user_story": 99,
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprints/" + str(sprint.pk) + "/mover_kanban/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["user_story"], ["No se encontró un user story en la base de datos"])

    def test_mover_kanban_con_estado_kanban_sin_especificar(self):
        """
        test_mover_kanban_con_estado_kanban_sin_especificar Prueba mover un user story a otra columna del kanban con estado kanban sin especificar
        """
        print("\nProbando mover un user story a otra columna del kanban con estado kanban sin especificar.")
        self.client.login(username="testing", password="polijira2021")
        sprint = Sprint.objects.get(pk=1)
        request_data = {
            "user_story": 1
        }
        response = self.client.post("/api/sprints/" + str(sprint.pk) + "/mover_kanban/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["estado_kanban"], ["No especificaste el estado del kanban"])

    def test_mover_kanban_con_estado_kanban_no_valido(self):
        """
        test_mover_kanban_con_estado_kanban_no_valido Prueba mover un user story a otra columna del kanban con estado kanban no válido
        """
        print("\nProbando mover un user story a otra columna del kanban con estado kanban no válido.")
        self.client.login(username="testing", password="polijira2021")
        sprint = Sprint.objects.get(pk=1)
        request_data = {
            "user_story": 99,
            "estado_kanban": "Z"
        }
        response = self.client.post("/api/sprints/" + str(sprint.pk) + "/mover_kanban/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 422)
        self.assertEquals(body["message"], "Error de validación")
        self.assertEquals(body["errors"]["estado_kanban"], ["Estado Kanban no válido"])

    def test_mover_kanban_con_sprint_sin_activar(self):
        """
        test_mover_kanban_con_sprint_sin_activar Prueba mover un user story a otra columna del kanban con sprint sin activar
        """
        print("\nProbando mover un user story a otra columna del kanban con sprint sin activar.")
        self.client.login(username="testing", password="polijira2021")
        sprint = Sprint.objects.get(pk=1)
        sprint.finalizar()
        request_data = {
            "user_story": 1,
            "estado_kanban": "D"
        }
        response = self.client.post("/api/sprints/" + str(sprint.pk) + "/mover_kanban/",
                                    request_data, content_type="application/json")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEquals(body["message"], "El kanban no se puede modificar en el estado actual del Sprint")
        self.assertEquals(body["error"], "forbidden")
