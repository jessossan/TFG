from django.db import models
from django.contrib import admin


# Create your models here.

class LikeDislike(models.Model):
    # Atributos de la clase LikeDislike: like

    like = models.BooleanField(default=False)

    # Relación con actor
    # Relación con comentario

    def __str__(self):
        return str(self.like)

    class Meta:
        verbose_name = "LikeDislike"
        verbose_name_plural = "LikesDislikes"


class LikeDislikeAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('like',)
