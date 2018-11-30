from django.db import models
from django.contrib import admin


# Create your models here.
from actors.models import Actor
from comments.models import Comment


class LikeDislike(models.Model):
    # Atributos de la clase LikeDislike: like

    like = models.BooleanField(default=False)

    # Relación con actor
    actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True)
    # Relación con comentario
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.like)

    class Meta:
        verbose_name = "LikeDislike"
        verbose_name_plural = "LikesDislikes"


class LikeDislikeAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('like', 'actor', 'comment')
