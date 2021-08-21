from rest_framework import viewsets, status
from rest_framework import response
from rest_framework.response import Response
from backend.api.models import Rol
from backend.api.serializers import RolSerializer


class RolViewSet(viewsets.ViewSet):
    """
    RolViewSet View para el modelo Rol

    Args:
        viewsets (module): tipo de clase basado en view
    """

    def list(self, request):
        """
        list Lista todos los roles del sistema

        Args:
            request (Any): request

        Return:
            json: lista de roles en formato json
        """
        # if (False):   #########CAMBIAR A SI EL USUARIO NO TIENE PERMISO
        #     response = {
        #         "message": "No tiene permisos para realizar esta acción"}
        #     return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        retrieve Obtiene un rol de sistema mediante su pk

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.

        Returns:
            json: rol obtenido en formato json
        """
        # if (False):    #########CAMBIAR A SI EL USUARIO NO TIENE PERMISO
        #    response = {
        #        "message": "No tiene permisos para realizar esta acción"}
        #    return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        try:
            rol = Rol.objects.get(pk=pk)
            serializer = RolSerializer(rol, many=False)
            return Response(serializer.data)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        create Crea un rol de sistema

        Args:
            request (Any): request

        Returns:
            json: rol creado en formato json
        """
        # if (False):    #########CAMBIAR A "SI EL USUARIO NO TIENE PERMISO"
        #    response = {
        #        "message": "No tiene permisos para realizar esta acción"}
        #    return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        rol = Rol.objects.create(nombre=request.data["nombre"])
        serializer = RolSerializer(rol, many=False)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        destroy Elimina un rol de sistema

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.
        """
        # if (False):   #########CAMBIAR A "SI EL USUARIO NO TIENE PERMISO"
        #    response = {
        #        "message": "No tiene permisos para realizar esta acción"}
        #    return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        try:
            rol = Rol.objects.get(pk=pk)
            rol.delete()
            response = {"message": "Rol Eliminado."}
            return Response(response)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        update Obtiene un rol de sistema mediante su pk

        Args:
            request (Any): request
            pk (integer, opcional): primary key. Defaults to None.

        Returns:
            json: rol modificado en formato json
        """
        # if (False):   #########CAMBIAR A "SI EL USUARIO NO TIENE PERMISO"
        #    response = {
        #        "message": "No tiene permisos para realizar esta acción"}
        #    return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        try:
            rol = Rol.objects.get(pk=pk)
            rol.nombre = request.data["nombre"]
            rol.save()
            serializer = RolSerializer(rol, many=False)
            return Response(serializer.data)
        except Rol.DoesNotExist:
            response = {"message": "No existe el rol"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
