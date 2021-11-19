from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Miembro, Proyecto, RolProyecto, Sprint, SprintBacklog, UserStory, Usuario, Horario
from backend.api.models.ProductBacklog import ProductBacklog
from backend.api.serializers import \
    ProyectoSerializer, \
    PermisoProyectoSerializer, \
    RolProyectoSerializer, \
    MiembroSerializer, \
    ImportarRolSerializer, \
    UserStorySerializer, \
    SprintSerializer, \
    ProductBacklogSerializer

from backend.api.forms import CreateProyectoForm, UpdateProyectoForm
from backend.api.decorators import FormValidator
from django.db import transaction
from django.db.models import Q

from backend.api.serializers.SprintBacklogSerializer import SprintBacklogSerializer


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
        if usuario_request.tiene_permiso("ver_proyectos"):
            proyectos = Proyecto.objects.all()
        else:
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
            proyecto = Proyecto.objects.get(pk=pk)
            if not usuario_request.tiene_permiso("ver_proyectos") and \
               not Miembro.es_miembro(usuario_request, proyecto):
                response = {
                    "message": "Debe ser miembro y tener permiso para realizar esta acción",
                    "permission_required": ["ver_proyectos"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
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
            miembro = Miembro.objects.get(rol__nombre="Scrum Master", proyecto=proyecto)
            horario = Horario.objects.create(
                lunes=0,
                martes=0,
                miercoles=0,
                jueves=0,
                viernes=0,
                sabado=0,
                domingo=0,
            )
            horario.asignar_horario(miembro)
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
            p = Proyecto.objects.filter(~Q(id=pk), nombre=request.data['nombre'])
            if len(p) > 0:
                response = {
                    "message": "Ya existe un proyecto con ese nombre",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro = Miembro.objects.get(rol__nombre="Scrum Master", proyecto=proyecto)
            miembro.horario.delete()
            proyecto.update(
                nombre=request.data['nombre'],
                fecha_inicio=request.data['fecha_inicio'],
                fecha_fin=request.data['fecha_fin'],
                scrum_master=scrum_master,
                scrum_master_handler=Miembro.actualizar_scrum_master
            )
            miembro = Miembro.objects.get(usuario=scrum_master, proyecto=proyecto)
            horario = Horario.objects.create(
                lunes=0,
                martes=0,
                miercoles=0,
                jueves=0,
                viernes=0,
                sabado=0,
                domingo=0,
            )
            horario.asignar_horario(miembro)
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
            proyecto = Proyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=proyecto)
            if not miembro.tiene_permiso("activar_proyecto"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["activar_proyecto"],
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

    @action(detail=True, methods=['GET'])
    def roles(self, request, pk=None):
        """
        list Lista todos los roles de proyecto del proyecto especificado

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Return:
            json: lista de roles de proyecto en formato json
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            proyecto = Proyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=proyecto)
            if not miembro.tiene_permiso("ver_roles_proyecto"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_roles_proyecto"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            roles = RolProyecto.objects.filter(proyecto=proyecto)
            serializer = RolProyectoSerializer(roles, many=True)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {
                "message": "El proyecto no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['GET'])
    def me(self, request, pk=None):
        """
        me Obtiene el modelo miembro del usuario logueado en el proyecto especificado

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Return:
            JSON: Miembro solicitado en formato json
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            proyecto = Proyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=proyecto)
            serializer = MiembroSerializer(miembro, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except Proyecto.DoesNotExist:
            response = {
                "message": "El proyecto no existe",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["GET"])
    def miembros(self, request, pk=None):
        """
        miembros Lista todos los miembros del proyecto especificado

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Returns:
            JSON: Miembros del proyecto especificado en formato json
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto_id=pk)
            if not miembro.tiene_permiso("ver_miembros"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_miembros"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.objects.get(pk=pk)
            miembros = Miembro.objects.filter(proyecto=proyecto)
            serializer = MiembroSerializer(miembros, many=True)
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

    @action(detail=True, methods=["GET"])
    def importar_rol(self, request, pk=None):
        """
        importar_rol Importa un rol de proyecto de otro proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Return:
            JSON: Roles de proyecto en formato json
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            proyecto = Proyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=proyecto)
            if not miembro.tiene_permiso("importar_rol_proyecto"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["importar_rol_proyecto"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            proyecto = Proyecto.objects.filter(~Q(pk=proyecto.pk))
            serializer = ImportarRolSerializer(proyecto, many=True)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {
                "message": "No existe el proyecto",
                "error": "not_found"
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    @importar_rol.mapping.post
    def crear_importado_rol(self, request, pk=None):
        """
        crear_importado_rol Clona un rol especificado de otro proyecto al proyecto

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Return:
            JSON: Rol nuevo importado en formato json
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            proyecto = Proyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto=proyecto)
            if not miembro.tiene_permiso("importar_rol_proyecto"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["importar_rol_proyecto"]
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            rol_importado = RolProyecto.objects.get(pk=request.data["id"])
            rol = RolProyecto.objects.create(nombre=rol_importado.nombre, proyecto=proyecto)
            permisos = rol_importado.permisos.all()
            for p in permisos:
                rol.agregar_permiso(p)
            serializer = RolProyectoSerializer(rol, many=False)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {
                "message": "No existe el proyecto",
                "error": "not_found"
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {"message": "Usted no es miembro de este proyecto"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["GET"])
    def user_stories(self, request, pk=None):
        """
        user_stories Lista todos los User Stories de este Proyecto

        Args:
            request (Any): Request del Usuario
            pk (int, optional): Primary Key del Proyecto. Defaults to None.

        Returns:
            list(JSON): Lista de todos los User Story de este Proyecto en formato JSON
        """
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            miembro_request = Miembro.objects.get(usuario=usuario_request, proyecto_id=pk)
            if not miembro_request.tiene_permiso("ver_user_stories"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "permission_required": ["ver_user_stories"],
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            user_stories = UserStory.objects.filter(product_backlogs__proyecto_id=pk)
            serializer = UserStorySerializer(user_stories, many=True)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "No existe el Proyecto",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["GET"])
    def sprints(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(usuario=usuario, proyecto_id=pk)
            if not miembro.tiene_permiso("ver_sprints"):
                sprints = Sprint.objects.filter(miembro_sprints__miembro_proyecto=miembro)
                serializer = SprintSerializer(sprints, many=True)
                return Response(serializer.data)
            sprints = Sprint.objects.filter(proyecto_id=pk)
            serializer = SprintSerializer(sprints, many=True)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["GET"])
    def product_backlogs(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(usuario=usuario, proyecto_id=pk)
            if not usuario.tiene_permiso("ver_proyectos") or \
               not miembro.tiene_permiso("ver_user_stories"):
                response = {
                    "message": "No tiene permiso para realizar esta acción",
                    "error": "forbidden"
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            product_backlogs = ProductBacklog.objects.filter(proyecto_id=pk)
            serializer = ProductBacklogSerializer(product_backlogs, many=True)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["GET"])
    def estimaciones_pendientes(self, request, pk=None):
        """
        estimaciones_pendientes Devuelve los Sprint Backlogs parcialmente estimados asignados al Usuario.

        Args:
            request (Any): Request que se solicita

        Returns:
            JSON: Sprint Backlogs
        """
        try:
            usuario = Usuario.objects.get(user=request.user)
            proyecto = Proyecto.objects.get(pk=pk)
            miembro = Miembro.objects.get(usuario=usuario, proyecto=proyecto)
            us = SprintBacklog.objects.filter(estado_estimacion='p', desarrollador__miembro_proyecto=miembro)
            serializer = SprintBacklogSerializer(us, many=True)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except Proyecto.DoesNotExist:
            response = {
                "message": "No existe el Proyecto",
                "error": "not_found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'])
    def finalizar(self, request, pk=None):
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto_id=pk)
            if not miembro.tiene_permiso("finalizar_proyecto"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["finalizar_proyecto"],
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
            sprints_activos = Sprint.objects.filter(proyecto=proyecto, estado='A')
            if len(sprints_activos) > 0:
                response = {
                    "message": "No puedes finalizar el Proyecto hasta que todos los Sprints esten finalizados",
                    "error": "bad_request"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            proyecto.finalizar()
            serializer = ProyectoSerializer(proyecto, many=False)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {"message": "El proyecto no existe"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    @action(detail=True, methods=['POST'])
    def cancelar(self, request, pk=None):
        try:
            usuario_request = Usuario.objects.get(user=request.user)
            miembro = Miembro.objects.get(usuario=usuario_request, proyecto_id=pk)
            if not miembro.tiene_permiso("cancelar_proyecto"):
                response = {
                    "message": "No tiene permiso para realizar esta accion",
                    "permission_required": ["cancelar_proyecto"],
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
            sprints_activos = Sprint.objects.filter(proyecto=proyecto, estado='A')
            for sprint in sprints_activos:
                sprint.finalizar()
            proyecto.cancelar()
            serializer = ProyectoSerializer(proyecto, many=False)
            return Response(serializer.data)
        except Proyecto.DoesNotExist:
            response = {"message": "El proyecto no existe"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Miembro.DoesNotExist:
            response = {
                "message": "Usted no es miembro de este Proyecto",
                "error": "forbidden"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
