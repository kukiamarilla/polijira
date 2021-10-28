from django.db import models


class Review(models.Model):
    """
    Review
    Modela el Review de User Stories

    Args:
        models (Model): Model de django

    Atributes:
        user_story (ForeignKey): User Story al que hace referencia el review
        observacion (TextField): Descripcion sobre el del User Story
        autor (ForeignKey): Miembro del proyecto que hace el review
    """
    user_story = models.ForeignKey("UserStory", on_delete=models.CASCADE, related_name="reviews")
    observacion = models.TextField()
    fecha_creacion = models.DateField()
    autor = models.ForeignKey("Usuario", on_delete=models.CASCADE, related_name="reviews")
