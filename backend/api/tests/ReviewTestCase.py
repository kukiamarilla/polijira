from backend.api.models.PermisoProyecto import PermisoProyecto
from backend.api.models.Proyecto import Proyecto
from backend.api.models import RolProyecto, Miembro, Usuario, UserStory, Review
from django.test import TestCase, Client
from django.db.models import Q

from backend.api.models.SprintBacklog import SprintBacklog


class ReviewTestCase(TestCase):
    """
    ReviewTestCase Prueba las funcionalidades de Review
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
        "backend/api/fixtures/testing/miembros.json",
        "backend/api/fixtures/testing/horarios.json",
        "backend/api/fixtures/testing/user-stories.json",
        "backend/api/fixtures/testing/product-backlogs.json",
        "backend/api/fixtures/testing/registro-user-stories.json",
        "backend/api/fixtures/testing/sprints.json",
        "backend/api/fixtures/testing/sprintbacklogs.json",
        "backend/api/fixtures/testing/miembrosprints.json",
        "backend/api/fixtures/testing/reviews.json"
    ]

    def setUp(self):
        """
        setUp Configura el testcase
        """
        self.client = Client()

    def test_obtener_review(self):
        """
        test_obtener_review
        Prueba obtener un review de user story especificado
        """
        print("\nProbando obtener un review de user story especificado.")
        self.client.login(username="testing", password="polijira2021")
        review = Review.objects.get(pk=1)
        response = self.client.get("/api/reviews/" + str(review.id) + "/")
        body = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEqual(body["id"], review.id)
        self.assertEqual(body["user_story"], review.user_story.pk)
        self.assertEqual(body["observacion"], review.observacion)

    def test_obtener_review_sin_permiso(self):
        """
        test_obtener_review_sin_permiso
        Prueba obtener un review de user story especificado sin permiso
        """
        print("\nProbando obtener un review de user story especificado sin permiso.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        review = Review.objects.get(pk=1)
        response = self.client.get("/api/reviews/" + str(review.id) + "/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEqual(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEqual(body["permission_required"], ["ver_user_stories"])
        self.assertEqual(body["error"], "forbidden")

    def test_obtener_review_con_review_inexistente(self):
        """
        test_obtener_review_con_review_inexistente
        Prueba obtener un review de user story especificado con review inexistente
        """
        print("\nProbando obtener un review de user story especificado con review inexistente.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.get("/api/reviews/99/")
        body = response.json()
        self.assertEquals(response.status_code, 404)
        self.assertEqual(body["message"], "No existe review del User Story")
        self.assertEqual(body["error"], "not_found")

    def test_obtener_review_sin_ser_miembro_del_proyecto(self):
        """
        test_obtener_review_sin_ser_miembro_del_proyecto
        Prueba obtener un review de user story especificado sin ser miembro del proyecto
        """
        print("\nProbando obtener un review de user story especificado sin ser miembro del proyecto.")
        self.client.login(username="user_test", password="polijira2021")
        review = Review.objects.get(pk=1)
        response = self.client.get("/api/reviews/" + str(review.id) + "/")
        body = response.json()
        self.assertEquals(response.status_code, 403)
        self.assertEqual(body["message"], "Usted no es miembro de este Proyecto")
        self.assertEqual(body["error"], "forbidden")

    def test_crear_review(self):
        """
        test_crear_review
        Prueba crear un review de user story
        """
        print("\nProbando crear un review de User Story.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "user_story": 2,
            "observacion": "Corregir modelo"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.post("/api/reviews/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["user_story"], request_data["user_story"])
        self.assertEqual(body["observacion"], request_data["observacion"])
        self.assertEqual(body["autor"]["user"]["username"], "testing")

    def test_crear_review_sin_permiso_ver_user_stories(self):
        """
        test_crear_review_sin_permiso_ver_user_stories
        Prueba crear un review de user story sin permiso ver user stories 
        """
        print("\nProbando crear un review de User Story sin permiso ver user stories.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        request_data = {
            "user_story": 2,
            "observacion": "Corregir modelo"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.post("/api/reviews/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEqual(body["permission_required"], ["ver_user_stories", "crear_reviews"])
        self.assertEqual(body["error"], "forbidden")

    def test_crear_review_sin_permiso_crear_reviews(self):
        """
        test_crear_review_sin_permiso_crear_reviews
        Prueba crear un review de user story sin permiso crear reviews
        """
        print("\nProbando crear un review de User Story sin permiso crear reviews.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="crear_reviews").delete()
        request_data = {
            "user_story": 2,
            "observacion": "Corregir modelo"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.post("/api/reviews/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEqual(body["permission_required"], ["ver_user_stories", "crear_reviews"])
        self.assertEqual(body["error"], "forbidden")

    def test_crear_review_con_user_story_no_pendiente(self):
        """
        test_crear_review_con_user_story_no_pendiente
        Prueba crear un review de user story con estado no pendiente 
        """
        print("\nProbando crear un review de User Story con estado no pendiente.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "user_story": 2,
            "observacion": "Corregir modelo"
        }
        user_story = UserStory.objects.get(pk=2)
        sprint_backlog = SprintBacklog.objects.get(user_story=user_story)
        sprint_backlog.sprint.activar()
        user_story.estado = "E"
        user_story.save()
        response = self.client.post("/api/reviews/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "No se puede crear review en el estado actual del User Story")
        self.assertEqual(body["error"], "forbidden")

    def test_crear_review_sin_sprint_activo(self):
        """
        test_crear_review_sin_sprint_activo
        Prueba crear un review de user story sin sprint en estado activo
        """
        print("\nProbando crear un review de User Story sin sprint en estado activo.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "user_story": 2,
            "observacion": "Corregir modelo"
        }
        response = self.client.post("/api/reviews/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "No se puede crear review si el user story no está en un sprint activo")
        self.assertEqual(body["error"], "forbidden")

    def test_crear_review_sin_ser_miembro(self):
        """
        test_crear_review_sin_ser_miembro
        Prueba crear un review de user story sin ser miembro
        """
        print("\nProbando crear un review de User Story sin ser miembro.")
        self.client.login(username="user_test", password="polijira2021")
        request_data = {
            "user_story": 2,
            "observacion": "Corregir modelo"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.post("/api/reviews/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "Usted no es miembro de este Proyecto")
        self.assertEqual(body["error"], "forbidden")

    def test_crear_review_con_user_story_sin_especificar(self):
        """
        test_crear_review_con_user_story_sin_especificar
        Prueba crear un review de User Story con user story sin especificar
        """
        print("\nProbando crear un review de User Story con user story sin especificar.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "observacion": "Corregir modelo"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.post("/api/reviews/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(body["message"], "Error de validación")
        self.assertEqual(body["errors"]["user_story"], ["No especificaste el user story"])

    def test_crear_review_con_observacion_sin_especificar(self):
        """
        test_crear_review_con_observacion_sin_especificar
        Prueba crear un review de User Story con observación sin especificar
        """
        print("\nProbando crear un review de User Story con observación sin especificar.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "user_story": 2
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.post("/api/reviews/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(body["message"], "Error de validación")
        self.assertEqual(body["errors"]["observacion"], ["No especificaste la observacion"])

    def test_crear_review_con_user_story_inexistente(self):
        """
        test_crear_review_con_user_story_inexistente
        Prueba crear un review de User Story con user story inexistente
        """
        print("\nProbando crear un review de User Story con user story inexistente.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "user_story": 99,
            "observacion": "Corregir modelo"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.post("/api/reviews/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(body["message"], "Error de validación")
        self.assertEqual(body["errors"]["user_story"], ["No se encontro el user story en la base de datos"])

    def test_modificar_review(self):
        """
        test_modificar_review
        Prueba modificar un review de user story
        """
        print("\nProbando modificar un review de User Story.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "observacion": "Volver a estimar horas"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.put("/api/reviews/1/", request_data, content_type="application/json")
        body = response.json()
        review = Review.objects.get(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["user_story"], review.user_story.pk)
        self.assertEqual(review.observacion, request_data["observacion"])
        self.assertEqual(body["autor"]["user"]["username"], "testing")

    def test_modificar_review_sin_ser_autor(self):
        """
        test_modificar_review_sin_ser_autor
        Prueba modificar un review de User Story sin ser autor
        """
        print("\nProbando modificar un review de User Story sin ser autor.")
        self.client.login(username="user_testing", password="polijira2021")
        request_data = {
            "observacion": "Volver a estimar horas"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.put("/api/reviews/1/", request_data, content_type="application/json")
        body = response.json()
        review = Review.objects.get(pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(review.observacion, request_data["observacion"])
        self.assertEqual(body["message"], "Usted no el autor de este review")
        self.assertEqual(body["error"], "forbidden")

    def test_modificar_review_sin_permiso_modificar_reviews(self):
        """
        test_modificar_review_sin_permiso_modificar_reviews
        Prueba modificar un review de user story sin permiso modificar reviews
        """
        print("\nProbando modificar un review de User Story sin permiso modificar reviews.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="modificar_reviews").delete()
        request_data = {
            "observacion": "Volver a estimar horas"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.put("/api/reviews/1/", request_data, content_type="application/json")
        body = response.json()
        review = Review.objects.get(pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(review.observacion, request_data["observacion"])
        self.assertEqual(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEqual(body["permission_required"], ["ver_user_stories", "modificar_reviews"])
        self.assertEqual(body["error"], "forbidden")

    def test_modificar_review_sin_permiso_ver_user_stories(self):
        """
        test_modificar_review_sin_permiso_ver_user_stories
        Prueba modificar un review de user story sin permiso ver user stories 
        """
        print("\nProbando modificar un review de User Story sin permiso ver user stories.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        request_data = {
            "user_story": 2,
            "observacion": "Volver a estimar horas"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.put("/api/reviews/1/", request_data, content_type="application/json")
        body = response.json()
        review = Review.objects.get(pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(review.observacion, request_data["observacion"])
        self.assertEqual(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEqual(body["permission_required"], ["ver_user_stories", "modificar_reviews"])
        self.assertEqual(body["error"], "forbidden")

    def test_modificar_review_con_user_story_no_pendiente(self):
        """
        test_modificar_review_con_user_story_no_pendiente
        Prueba modificar un review de user story con estado no pendiente 
        """
        print("\nProbando modificar un review de User Story con estado no pendiente.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "observacion": "Corregir modelo"
        }
        user_story = UserStory.objects.get(pk=2)
        sprint_backlog = SprintBacklog.objects.get(user_story=user_story)
        sprint_backlog.sprint.activar()
        user_story.estado = "E"
        user_story.save()
        response = self.client.put("/api/reviews/1/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "No se puede modificar review en el estado actual del User Story")
        self.assertEqual(body["error"], "forbidden")

    def test_modificar_review_sin_sprint_activo(self):
        """
        test_modificar_review_sin_sprint_activo
        Prueba modificar un review de user story sin sprint en estado activo
        """
        print("\nProbando modificar un review de User Story sin sprint en estado activo.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "observacion": "Volver a estimar horas"
        }
        response = self.client.put("/api/reviews/1/", request_data, content_type="application/json")
        body = response.json()
        review = Review.objects.get(pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(review.observacion, request_data["observacion"])
        self.assertEqual(body["message"], "No se puede modificar review si el user story no está en un sprint activo")
        self.assertEqual(body["error"], "forbidden")

    def test_modificar_review_con_observacion_sin_especificar(self):
        """
        test_modificar_review_con_observacion_sin_especificar
        Prueba modificar un review de User Story con observación sin especificar
        """
        print("\nProbando modificar un review de User Story con observación sin especificar.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {}
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.put("/api/reviews/1/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(body["message"], "Error de validación")
        self.assertEqual(body["errors"]["observacion"], ["No especificaste la observacion"])

    def test_modificar_review_con_review_inexistente(self):
        """
        test_modificar_review_con_review_inexistente
        Prueba modificar un review de user story con review inexistente
        """
        print("\nProbando modificar un review de User Story con review inexistente.")
        self.client.login(username="testing", password="polijira2021")
        request_data = {
            "observacion": "Volver a estimar horas"
        }
        response = self.client.put("/api/reviews/99/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body["message"], "No existe el review especificado")
        self.assertEqual(body["error"], "not_found")

    def test_modificar_review_sin_ser_miembro(self):
        """
        test_modificar_review_sin_ser_miembro
        Prueba modificar un review de user story sin ser miembro
        """
        print("\nProbando modificar un review de User Story sin ser miembro.")
        self.client.login(username="user_test", password="polijira2021")
        request_data = {
            "observacion": "Corregir modelo"
        }
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.put("/api/reviews/1/", request_data, content_type="application/json")
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body["message"], "Usted no es miembro de este Proyecto")
        self.assertEqual(body["error"], "forbidden")

    def test_eliminar_review(self):
        """
        test_eliminar_review
        Prueba eliminar un review de user story
        """
        print("\nProbando eliminar un review de User Story.")
        self.client.login(username="testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.delete("/api/reviews/1/")
        body = response.json()
        review = Review.objects.filter(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(review), 0)
        self.assertEqual(body["message"], "Review eliminado")

    def test_eliminar_review_sin_ser_autor(self):
        """
        test_eliminar_review_sin_ser_autor
        Prueba eliminar un review de User Story sin ser autor
        """
        print("\nProbando eliminar un review de User Story sin ser autor.")
        self.client.login(username="user_testing", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.delete("/api/reviews/1/")
        body = response.json()
        review = Review.objects.filter(pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(len(review), 0)
        self.assertEqual(body["message"], "Usted no el autor de este review")
        self.assertEqual(body["error"], "forbidden")

    def test_eliminar_review_sin_permiso_eliminar_reviews(self):
        """
        test_eliminar_review_sin_permiso_eliminar_reviews
        Prueba eliminar un review de user story sin permiso eliminar reviews
        """
        print("\nProbando eliminar un review de User Story sin permiso eliminar reviews.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="eliminar_reviews").delete()
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.delete("/api/reviews/1/")
        body = response.json()
        review = Review.objects.filter(pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(len(review), 0)
        self.assertEqual(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEqual(body["permission_required"], ["ver_user_stories", "eliminar_reviews"])
        self.assertEqual(body["error"], "forbidden")

    def test_eliminar_review_sin_permiso_ver_user_stories(self):
        """
        test_eliminar_review_sin_permiso_ver_user_stories
        Prueba eliminar un review de user story sin permiso ver user stories
        """
        print("\nProbando eliminar un review de User Story sin permiso ver user stories.")
        self.client.login(username="testing", password="polijira2021")
        PermisoProyecto.objects.get(codigo="ver_user_stories").delete()
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.delete("/api/reviews/1/")
        body = response.json()
        review = Review.objects.filter(pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(len(review), 0)
        self.assertEqual(body["message"], "No tiene permiso para realizar esta acción")
        self.assertEqual(body["permission_required"], ["ver_user_stories", "eliminar_reviews"])
        self.assertEqual(body["error"], "forbidden")

    def test_eliminar_review_con_user_story_no_pendiente(self):
        """
        test_eliminar_review_con_user_story_no_pendiente
        Prueba eliminar un review de user story con estado no pendiente 
        """
        print("\nProbando eliminar un review de User Story con estado no pendiente.")
        self.client.login(username="testing", password="polijira2021")
        user_story = UserStory.objects.get(pk=2)
        sprint_backlog = SprintBacklog.objects.get(user_story=user_story)
        sprint_backlog.sprint.activar()
        user_story.estado = "E"
        user_story.save()
        response = self.client.delete("/api/reviews/1/")
        body = response.json()
        review = Review.objects.filter(pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(len(review), 0)
        self.assertEqual(body["message"], "No se puede eliminar review en el estado actual del User Story")
        self.assertEqual(body["error"], "forbidden")

    def test_eliminar_review_sin_sprint_activo(self):
        """
        test_eliminar_review_sin_sprint_activo
        Prueba eliminar un review de user story sin sprint en estado activo
        """
        print("\nProbando eliminar un review de User Story sin sprint en estado activo.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/reviews/1/")
        body = response.json()
        review = Review.objects.filter(pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(len(review), 0)
        self.assertEqual(body["message"], "No se puede eliminar review si el user story no está en un sprint activo")
        self.assertEqual(body["error"], "forbidden")

    def test_eliminar_review_con_review_inexistente(self):
        """
        test_eliminar_review_con_review_inexistente
        Prueba eliminar un review de user story con review inexistente
        """
        print("\nProbando eliminar un review de User Story con review inexistente.")
        self.client.login(username="testing", password="polijira2021")
        response = self.client.delete("/api/reviews/99/")
        body = response.json()
        review = Review.objects.filter(pk=1)
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(len(review), 0)
        self.assertEqual(body["message"], "No existe el review especificado")
        self.assertEqual(body["error"], "not_found")

    def test_eliminar_review_sin_ser_miembro(self):
        """
        test_eliminar_review_sin_ser_miembro
        Prueba eliminar un review de user story sin ser miembro
        """
        print("\nProbando eliminar un review de User Story sin ser miembro.")
        self.client.login(username="user_test", password="polijira2021")
        sprint_backlog = SprintBacklog.objects.get(user_story=UserStory.objects.get(pk=2))
        sprint_backlog.sprint.activar()
        response = self.client.delete("/api/reviews/1/")
        body = response.json()
        review = Review.objects.filter(pk=1)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(len(review), 0)
        self.assertEqual(body["message"], "Usted no es miembro de este Proyecto")
        self.assertEqual(body["error"], "forbidden")
