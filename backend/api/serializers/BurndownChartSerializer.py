from rest_framework import serializers
from backend.api.models import BurndownChart


class BurndownChartSerializer(serializers.ModelSerializer):
    """
    BurndownChartSerializer Serializa los datos de Burndown Chart

    Args:
        serializers (ModelSerializer): Serializador del módulo Rest Framework
    """

    class Meta:
        """
         Metadatos de Burndown Chart
        """
        model = BurndownChart
        fields = ("x", "y")
