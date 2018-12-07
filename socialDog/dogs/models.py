from django.core.validators import MinValueValidator
from django.db import models
from django.contrib import admin
from breeds.models import Breed


# Create your models here.


class Dog(models.Model):
    # Atributos de la clase Dog: name, age, gender, breed, descendant, details, photo, awards

    # Tipos de género
    MALE = 'Macho'
    FEMALE = 'Hembra'
    GenderType = (
        (MALE, 'Macho'),
        (FEMALE, 'Hembra'),
    )
    name = models.CharField(max_length=50, unique=True, help_text="Requerido. 50 carácteres como máximo")
    age = models.PositiveIntegerField(default=0, help_text="Edad, requerido",
                                      validators=[MinValueValidator(0)])
    gender = models.CharField(max_length=10, choices=GenderType)
    descendant = models.CharField(max_length=200, help_text="Descendencia, no requerido", null=True, blank=True)
    details = models.CharField(max_length=200, help_text="Detalles, no requerido", null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='uploads/')  # Donde va uploads?
    awards = models.CharField(max_length=200, help_text="Premios, no requerido", null=True, blank=True)

    # Relación con raza
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)

    # Relación con criador
    breeder = models.ForeignKey('actors.Breeder', on_delete=models.CASCADE, null=True)
    # Relación con comentario

    # Relación con valoración

    def __str__(self):
        return str(self.name) + ' - ' + str(self.breed) + ' - ' + str(self.age) + ' - ' + str(self.gender) + ' - ' + str(self.descendant) + \
               ' - ' + str(self.details) + ' - ' + str(self.awards)

    class Meta:
        verbose_name = "Perro"
        verbose_name_plural = "Perros"


class DogAdminPanel(admin.ModelAdmin):  # Falta BREED
    # Panel de admin
    list_display = ('name', 'breed','age', 'gender', 'descendant', 'details', 'awards')
