from django.core.validators import MinValueValidator
from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.

class Dog(models.Model):
    #Atributos de la clase Dog: name, age, gender, breed, descendant, details, photo, awards

    #Tipos de género
    MALE = 'Macho'
    FEMALE = 'Hembra'
    GenderType = (
        (MALE, 'Macho'),
        (FEMALE, 'Hembra'),
    )
    name = models.CharField(max_length=50, help_text="Requerido. 50 carácteres como máximo")
    age = models.PositiveIntegerField(default=0, verbose_name='Edad', validators=[MinValueValidator(0)]) #Y si son meses que?
    gender = models.CharField(max_length=10, choices=GenderType)
    #breed =
    descendant = models.CharField(max_length=200, help_text="Descendencia", null=True, blank=True)
    details = models.CharField(max_length=200, help_text="Detalles", null=True, blank=True)
    photo = models.ImageField(null = True, blank = True, upload_to = 'uploads/') # Donde va uploads?
    awards = models.CharField(max_length=200, help_text="Premios", null=True, blank=True)
    #Relaciones

    def __str__(self):
        return str(self.name) + ' - ' + str(self.age) + ' - ' + str(self.gender) + ' - ' + str(self.descendant) + \
               ' - ' + str(self.details) + ' - ' + str(self.awards)

    class Meta:
        verbose_name = "Perro"
        verbose_name_plural = "Perros"

class DogAdminPanel(admin.ModelAdmin): #Falta BREED
    #Panel de admin
    list_display = ('name', 'age', 'gender', 'descendant', 'details', 'awards')

