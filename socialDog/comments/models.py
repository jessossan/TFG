from django.core.validators import MinValueValidator
from django.db import models
from django.contrib import admin


# Create your models here.

class Comment(models.Model):
    # Atributos de la clase Comment: title, text, creationDate, likes, dislikes
    title = models.CharField(max_length=50, help_text="Requerido. 50 carácteres como máximo")
    text = models.CharField(max_length=200, help_text="Requerido. 200 carácteres como máximo")
    creationDate = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)])
    dislikes = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    # Relación con asociación
    # Relación con criador
    # Relación con evento
    # Relación con perro
    # Relación con noticia

    def __str__(self):
        return str(self.title) + ' - ' + str(self.text) + ' - ' + str(self.creationDate)+ ' - ' \
               + str(self.likes) + ' - ' + str(self.dislikes)

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"


class CommentAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('title', 'text', 'creationDate', 'likes', 'dislikes',)
