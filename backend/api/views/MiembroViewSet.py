from rest_framework import viewsets, status
from rest_framework.response import Response
from backend.api.models import Usuario, Miembro, Proyecto, RolProyecto
from backend.api.serializers import MiembroSerializer


class MiembroViewSet(viewsets.ViewSet):
    """
    MiembroViewSet View para el modelo de Miembro

    Args:
        viewsets (ViewSet): Tipo de clase basado en View
    """

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene un miembro por su pk

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key

        Return:
            JSON: Miembro con la pk especificada
        """
        try:
            rol = Miembro.objects.get(pk=pk)
            serializer = MiembroSerializer(rol, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {"message": "No existe el miembro"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        create Crea un miembro nuevo

        Args:
            request (Any): request

        Return:
            JSON: Miembro creado
        """
        try:
            usuario = Usuario.objects.get(pk=request.data["usuario"])
            proyecto = Proyecto.objects.get(pk=request.data["proyecto"])
            rol = RolProyecto.objects.get(pk=request.data["rol"])
            if rol.proyecto != proyecto:
                response = {"message": "Rol no pertenece al proyecto"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro = Miembro.objects.create(usuario=usuario, proyecto=proyecto, rol=rol)
            serializer = MiembroSerializer(miembro, many=False)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            response = {"message": "No existe el usuario"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Proyecto.DoesNotExist:
            response = {"message": "No existe el proyecto"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except RolProyecto.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        destroy Elimina un miembro con la pk especificada

        Args:
            request (Any): request
            pk (integer, opcional): Primary Key del miembro a eliminar
        """
        try:
            miembro = Miembro.objects.get(pk=pk)
            miembro.delete()
            response = {"message": "Miembro Eliminado."}
            return Response(response)
        except Miembro.DoesNotExist:
            response = {"message": "No existe el miembro"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        update Modifica un miembro con la pk especificada

        Args:
            request (Any): request
            pk (integer, opcional): Primary key del miembro a modificar
        """
        try:
            miembro = Miembro.objects.get(pk=pk)
            rol = RolProyecto.objects.get(pk=request.data["rol"])
            if rol.proyecto != miembro.proyecto:  # form
                response = {"message": "Rol no pertenece al proyecto"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            miembro.rol = rol
            miembro.save()
            serializer = MiembroSerializer(miembro, many=False)
            return Response(serializer.data)
        except Miembro.DoesNotExist:
            response = {"message": "No existe el miembro"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except RolProyecto.DoesNotExist:  # form
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    # def horario(self, request, pk=None):
    # def capacidad(self, request, pk=None):
