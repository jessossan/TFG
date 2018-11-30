from django.db import models
from django.contrib import admin


# Create your models here.


class News(models.Model):
    # Atributos de la clase News: title, description, creationDate

    title = models.CharField(max_length=50, help_text="Requerido. 50 carácteres como máximo")
    description = models.CharField(max_length=200, help_text="Requerido. 200 carácteres como máximo")
    creationDate = models.DateTimeField(auto_now_add=True)

    # Relacion con actor asociación
    association = models.ForeignKey('actors.Association', on_delete=models.CASCADE, null=True, blank=True)
    # Relacion con actor que valoración
    # Relacion con actor criador
    breeder = models.ForeignKey('actors.Breeder', on_delete=models.CASCADE,null=True, blank=True)

    # Relacion con actor que comentario

    def __str__(self):
        return str(self.title) + ' - ' + str(self.description) + ' - ' + str(self.creationDate)

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"


class NewsAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('title', 'description', 'creationDate')
