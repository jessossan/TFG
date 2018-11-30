from django.core.validators import MinValueValidator
from django.db import models
from django.contrib import admin

# Create your models here.
from actors.models import Actor
from dogs.models import Dog
from events.models import Event
from news.models import News


class Comment(models.Model):
    # Atributos de la clase Comment: title, text, creationDate, likes, dislikes
    title = models.CharField(max_length=50, help_text="Requerido. 50 carácteres como máximo")
    text = models.CharField(max_length=200, help_text="Requerido. 200 carácteres como máximo")
    creationDate = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    dislikes = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    # Relación con asociación
    association = models.ForeignKey('actors.Association', on_delete=models.SET_NULL, null=True, blank=True)
    # Relación con criador
    breeder = models.ForeignKey('actors.Breeder', on_delete=models.SET_NULL, null=True, blank=True)
    # Relación con evento
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    # Relación con perro
    dog = models.ForeignKey(Dog, on_delete=models.SET_NULL, null=True, blank=True)
    # Relación con noticia
    news = models.ForeignKey(News, on_delete=models.SET_NULL, null=True, blank=True)
    # Relación con actor
    creator_comment = models.ForeignKey(Actor, verbose_name='Creator', on_delete=models.SET_NULL, null=True, related_name='creator_comment')

    def __str__(self):
        return str(self.title) + ' - ' + str(self.text) + ' - ' + str(self.creationDate) + ' - ' \
               + str(self.likes) + ' - ' + str(self.dislikes)

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"


class CommentAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('title', 'text', 'creationDate', 'creator_comment', 'likes')
