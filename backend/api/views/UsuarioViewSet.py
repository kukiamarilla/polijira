import json
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User, Group
from backend.api.models import Usuario
from backend.api.serializers import UsuarioSerializer
from django.shortcuts import get_object_or_404


class UsuarioViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['GET'])
    def me(self, request):
        """Obtiene el usuario autenticado

        Args:
            request (Any): request
        """
        user = self.request.user
        usuario = Usuario.objects.get(user=user)
        serializer = UsuarioSerializer(usuario, many=False)
        return Response(serializer.data)
