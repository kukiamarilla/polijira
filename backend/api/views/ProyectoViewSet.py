from backend.api.decorators.FormValidator import FormValidator
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Proyecto, Usuario
from backend.api.serializers import ProyectoSerializer
from backend.api.forms import CreateProyectoForm
from backend.api.decorators import FormValidator


class ProyectoViewSet(viewsets.ViewSet):
    """
    ProyectoViewSet View para el modelo Proyecto
    """

    def list(self, request):
        """
        list Lista todos los proyectos

        Args:
            request (Any): request

        Returns:
            json: Proyecto[]
        """
        usuario_request = Usuario.objects.get(user=request.user)
        if not usuario_request.tiene_permiso("ver_proyectos"):
            # Falta el modelo Miembro para traer los proyectos al que pertenece
            return
        proyectos = Proyecto.objects.all()
        serializer = ProyectoSerializer(proyectos, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene un proyecto

        Args:
            request (Any): request
            pk (integer, optional): primary key. Defaults to None.

        Returns:
            json: Proyecto
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("ver_proyectos"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["ver_proyectos"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.objects.get(pk=pk)
            serializer = ProyectoSerializer(proyecto, many=False)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {
                "message": "No existe el proyecto",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @FormValidator(form=CreateProyectoForm)
    def create(self, request):
        """
        create Crea un proyecto

        Args:
            request (Any): request

        Returns:
            json: Proyecto
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("crear_proyectos") and \
                    not usuario_request.tiene_permiso("ver_usuarios"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["crear_proyectos", "ver_usuarios"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.objects.create(
                nombre=request.data['nombre'],
                fecha_inicio=request.data['fecha_inicio'],
                fecha_fin=request.data['fecha_fin'],
                scrum_master=Usuario.objects.get(pk=request.data['scrum_master_id'])
            )
            # Falta agregar al scrum master como miembro del proyecto
            # Falta agregar el rol de proyecto scrum master al usuario asignado como scrum master
            serializer = ProyectoSerializer(proyecto, many=False)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            response = {
                "message": "No existe el Scum Master",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        update Modifica un Proyecto

        Args:
            request (Any): request
            pk (integer, optional): primary key. Defaults to None.

        Returns:
            json: Proyecto
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("modificar_proyectos") and \
               not usuario_request.tiene_permiso("ver_proyectos") and \
               not usuario_request.tiene_permiso("ver_usuarios"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": [
                        "modificar_proyectos",
                        "ver_proyectos",
                        "ver_usuarios"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.objects.get(pk=pk)
            if proyecto.estado != 'P':
                response = {
                    "message": "No puedes modificar el Proyecto en su estado actual",
                    "estado": dict(proyecto.ESTADO)[proyecto.estado],
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            Proyecto.objects.filter(pk=pk).update(**request.data)
            # Falta verificar si se agrega un nuevo scrum master, si es asi
            # el scrum master anterior deja de ser miembro del proyecto; y
            # el nuevo pasa a ser miembro del proyecto
            proyecto = Proyecto.objects.get(pk=pk)
            serializer = ProyectoSerializer(proyecto, many=False)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {"message": "El proyecto no existe"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        destroy Elimina un Proyecto

        Args:
            request (Any): request
            pk (integer, optional): primary key. Defaults to None.

        Returns:
            http request: 200
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("ver_proyectos") and \
               not usuario_request.tiene_permiso("eliminar_proyectos"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": [
                        "ver_proyectos",
                        "eliminar_proyectos"
                    ],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.objects.get(pk=pk)
            if proyecto.estado != 'P':
                response = {
                    "message": "No puedes eliminar el Proyecto en su estado actual",
                    "estado": dict(proyecto.ESTADO)[proyecto.estado],
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            proyecto.delete()
            response = {"message": "Proyecto Eliminado"}
            return Response(response, status=status.HTTP_200_OK)
        except Proyecto.DoesNotExist:
            response = {"message": "El proyecto no existe"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def activar(self, request, pk=None):
        """
        activar Activa el Proyecto

        Args:
            request (Any): request
            pk (integer, optional): primary key. Defaults to None.

        Returns:
            json: Proyecto
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("activar_proyectos"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["activar_proyectos"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.objects.get(pk=pk)
            if proyecto.estado != 'P':
                response = {
                    "message": "No puedes activar el Proyecto en su estado actual",
                    "estado": dict(proyecto.ESTADO)[proyecto.estado],
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            proyecto.iniciar()
            serializer = ProyectoSerializer(proyecto, many=False)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {"message": "El proyecto no existe"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def finalizar(self, request, pk=None):
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("finalizar_proyectos"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["finalizar_proyectos"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.objects.get(pk=pk)
            if proyecto.estado != 'A':
                response = {
                    "message": "No puedes finalizar el Proyecto en su estado actual",
                    "estado": dict(proyecto.ESTADO)[proyecto.estado],
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            proyecto.finalizar()
            serializer = ProyectoSerializer(proyecto, many=False)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {"message": "El proyecto no existe"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def cancelar(self, request, pk=None):
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            if not usuario_request.tiene_permiso("cancelar_proyectos"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["cancelar_proyectos"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.objects.get(pk=pk)
            if proyecto.estado != 'A':
                response = {
                    "message": "No puedes cancelar el Proyecto en su estado actual",
                    "estado": dict(proyecto.ESTADO)[proyecto.estado],
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            proyecto.cancelar()
            serializer = ProyectoSerializer(proyecto, many=False)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {"message": "El proyecto no existe"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
