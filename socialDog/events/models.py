from django.core.validators import MinValueValidator
from django.db import models
from django.contrib import admin


# Create your models here.

class Event(models.Model):
    # Atributos de la clase Event: title, description, place, creationDate, startDate, finishDate, length
    title = models.CharField(max_length=50, unique=True, help_text="Requerido. 50 carácteres como máximo")
    description = models.CharField(max_length=50, help_text="Requerido. 50 carácteres como máximo")
    place = models.CharField(max_length=100, help_text="Requerido. 100 carácteres como máximo")
    creationDate = models.DateTimeField(auto_now_add=True)
    startDate = models.DateTimeField()
    finishDate = models.DateTimeField()
    length = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    # Relación con comentario
    # Relación con criador
    breeder = models.ForeignKey('actors.Breeder', on_delete=models.CASCADE, null=True, blank=True)
    # Relación con asociación
    association = models.ForeignKey('actors.Association', on_delete=models.CASCADE, null=True, blank=True)
    # Relación con valoración

    def __str__(self):
        return str(self.title) + ' - ' + str(self.description) + ' - ' + str(self.place) + ' - ' + str(
            self.creationDate) \
               + ' - ' + str(self.startDate) + ' - ' + str(self.finishDate) + ' - ' + str(self.length)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"


class EventAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('title', 'description', 'place', 'creationDate', 'startDate', 'finishDate', 'length',)
