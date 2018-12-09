from django.db import models
from django.contrib import admin


# Create your models here.

class Breed(models.Model):
    # Atributos de la clase Breed: name, photo, classificationFCI
    name = models.CharField(max_length=50, unique=True, help_text="Requerido. 50 carácteres como máximo")

    # Sin Relaciones

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Raza"
        verbose_name_plural = "Razas"


class BreedAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('name',)
