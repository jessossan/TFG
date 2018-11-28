from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib import admin


# Create your models here.


class Rate(models.Model):
    # Atributos de la clase Rate: stars, description

    stars = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    description = models.CharField(max_length=200, help_text="Requerido. 200 carácteres como máximo")

    # Relacion con asociación
    # Relacion con evento
    # Relacion con criador
    # Relación con noticia
    # Relación con perro

    def __str__(self):
        return str(self.stars) + ' - ' + str(self.description)

    class Meta:
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"


class RateAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('stars', 'description')
