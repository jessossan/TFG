from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib import admin


# Create your models here.
from actors.models import Actor
from dogs.models import Dog
from events.models import Event
from news.models import News


class Rate(models.Model):
    # Atributos de la clase Rate: stars, description

    stars = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    description = models.CharField(max_length=200, help_text="Requerido. 200 carácteres como máximo")
    creationDate = models.DateTimeField(auto_now_add=True)

    # Relacion con asociación
    association = models.ForeignKey('actors.Association', on_delete=models.CASCADE, null=True, blank=True)
    # Relacion con evento
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    # Relacion con criador
    breeder = models.ForeignKey('actors.Breeder', on_delete=models.CASCADE, null=True, blank=True)
    # Relación con noticia
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True, blank=True)
    # Relación con perro
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, null=True, blank=True)
    # Relación con actor
    creator_rate = models.ForeignKey(Actor, verbose_name='Creator', on_delete=models.SET_NULL, null=True, related_name='creator_rate')


    def __str__(self):
        return str(self.stars) + ' - ' + str(self.description) + str(self.creationDate)

    class Meta:
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"


class RateAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('stars', 'description', 'creator_rate', 'creationDate')
