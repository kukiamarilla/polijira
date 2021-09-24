from django.db import models


class ProductBacklog(models.Model):
    proyecto = models.OneToOneField("Proyecto", on_delete=models.CASCADE, related_name="product_backlog")
    user_story = models.ForeignKey("UserStory", on_delete=models.CASCADE, related_name="product_backlogs")

    @staticmethod
    def almacenar_user_story(user_story, proyecto):
        ProductBacklog.objects.create(
            proyecto=proyecto,
            user_story=user_story
        )
        user_story.product_backlog = True
        user_story.save()