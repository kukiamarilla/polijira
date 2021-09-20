from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Miembro, Proyecto, RolProyecto, Usuario
from backend.api.serializers import ProyectoSerializer, PermisoProyectoSerializer
from backend.api.forms import CreateProyectoForm, UpdateProyectoForm
from backend.api.decorators import FormValidator
from django.db import transaction


class ProyectoViewSet(viewsets.ViewSet):
    """
    ProyectoViewSet View para el modelo Proyecto
    """

    def list(self, request):
        """
        list Lista todos los proyectos al que el usuario pertenece

        Args:
            request (Any): request

        Returns:
            json: Proyecto[]
        """
        usuario_request = Usuario.objects.get(user=request.user)
        proyectos = Proyecto.objects.filter(miembros__usuario=usuario_request)
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

    @transaction.atomic
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
            if not usuario_request.tiene_permiso("crear_proyectos") or \
               not usuario_request.tiene_permiso("ver_usuarios"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["crear_proyectos", "ver_usuarios"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.create(
                nombre=request.data['nombre'],
                fecha_inicio=request.data['fecha_inicio'],
                fecha_fin=request.data['fecha_fin'],
                scrum_master=Usuario.objects.get(pk=request.data['scrum_master_id']),
                roles_handler=RolProyecto.from_plantilla,
                scrum_master_handler=Miembro.asignar_scrum_master
            )
            serializer = ProyectoSerializer(proyecto, many=False)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            response = {
                "message": "No existe el usuario asignado como Scrum Master",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    @FormValidator(UpdateProyectoForm)
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
            if not usuario_request.tiene_permiso("modificar_proyectos") or \
               not usuario_request.tiene_permiso("ver_proyectos") or \
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
                    "message": "Solo puedes modificar un proyecto en estado Pendiente",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            scrum_master = Usuario.objects.get(pk=request.data["scrum_master_id"])
            proyecto.update(
                nombre=request.data['nombre'],
                fecha_inicio=request.data['fecha_inicio'],
                fecha_fin=request.data['fecha_fin'],
                scrum_master=scrum_master,
                scrum_master_handler=Miembro.actualizar_scrum_master
            )
            serializer = ProyectoSerializer(proyecto, many=False)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {
                "message": "El proyecto no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Usuario.DoesNotExist:
            response = {
                "message": "No existe el Scrum Master",
                "error": "not_found"
            }
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
            if not usuario_request.tiene_permiso("ver_proyectos") or \
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
                    "message": "El proyecto debe estar en estado Pendiente para ser eliminado",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            proyecto.delete()
            response = {"message": "Proyecto Eliminado"}
            return Response(response, status=status.HTTP_200_OK)
        except Proyecto.DoesNotExist:
            response = {
                "message": "El proyecto no existe",
                "error": "not_found"
            }
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
            # if not usuario_request.tiene_permiso("activar_proyectos"):
            #     response = {
            #         "message": "No tiene permiso para realizar esta accion",
            #         "permission_required": ["activar_proyectos"],
            #         "error": "forbidden"
            #     }
            #     return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.objects.get(pk=pk)
            if proyecto.scrum_master.id != usuario_request.id:
                response = {
                    "message": "Debe ser Scrum Master para realizar esta accion",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            if proyecto.estado != 'P' and proyecto.estado != "A":
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
            response = {
                "message": "El proyecto no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["GET"])
    def mis_permisos(self, request, pk=None):

        try:
            usuario_request = Usuario.objects.get(user=request.user)
            proyecto = Proyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=proyecto)
            rol = miembro.rol
            serializer = PermisoProyectoSerializer(rol.permisos.all())
            return Response(serializer.data)

        except Proyecto.DoesNotExist:
            response = {
                "message": "No existe el proyecto",
                "error": "not_found"
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este proyecto",
                "error": "forbidden"
            }
            return Response(response, status.HTTP_403_FORBIDDEN)

    # @action(detail=True, methods=['POST'])
    # def finalizar(self, request, pk=None):
    #     try:
    #         usuario_request = Usuario.objects.get(user=request.user)
    #         if not usuario_request.tiene_permiso("finalizar_proyectos"):
    #             response = {
    #                 "message": "No tiene permiso para realizar esta accion",
    #                 "permission_required": ["finalizar_proyectos"],
    #                 "error": "forbidden"
    #             }
    #             return Response(response, status=status.HTTP_403_FORBIDDEN)
    #         proyecto = Proyecto.objects.get(pk=pk)
    #         if proyecto.estado != 'A':
    #             response = {
    #                 "message": "No puedes finalizar el Proyecto en su estado actual",
    #                 "estado": dict(proyecto.ESTADO)[proyecto.estado],
    #                 "error": "bad_request"
    #             }
    #             return Response(response, status=status.HTTP_400_BAD_REQUEST)
    #         proyecto.finalizar()
    #         serializer = ProyectoSerializer(proyecto, many=False)
    #         return Response(serializer.data)
    #     except Proyecto.DoesNotExist:
    #         response = {"message": "El proyecto no existe"}
    #         return Response(response, status=status.HTTP_404_NOT_FOUND)

    # @action(detail=True, methods=['POST'])
    # def cancelar(self, request, pk=None):
    #     try:
    #         usuario_request = Usuario.objects.get(user=request.user)
    #         if not usuario_request.tiene_permiso("cancelar_proyectos"):
    #             response = {
    #                 "message": "No tiene permiso para realizar esta accion",
    #                 "permission_required": ["cancelar_proyectos"],
    #                 "error": "forbidden"
    #             }
    #             return Response(response, status=status.HTTP_403_FORBIDDEN)
    #         proyecto = Proyecto.objects.get(pk=pk)
    #         if proyecto.estado != 'A':
    #             response = {
    #                 "message": "No puedes cancelar el Proyecto en su estado actual",
    #                 "estado": dict(proyecto.ESTADO)[proyecto.estado],
    #                 "error": "bad_request"
    #             }
    #             return Response(response, status=status.HTTP_400_BAD_REQUEST)
    #         proyecto.cancelar()
    #         serializer = ProyectoSerializer(proyecto, many=False)
    #         return Response(serializer.data)
    #     except Proyecto.DoesNotExist:
    #         response = {"message": "El proyecto no existe"}
    #         return Response(response, status=status.HTTP_404_NOT_FOUND)
