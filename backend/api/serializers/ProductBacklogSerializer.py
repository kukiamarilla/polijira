from rest_framework import serializers
from backend.api.models import ProductBacklog
from backend.api.serializers import UserStorySerializer


class ProductBacklogSerializer(serializers.ModelSerializer):
    user_story = UserStorySerializer(many=False, read_only=True)

    class Meta:
        model = ProductBacklog
        fields = (
            "id",
            "proyecto",
            "user_story"
        )
