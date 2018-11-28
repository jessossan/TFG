from django.db import models
from django.contrib import admin


# Create your models here.


class Request(models.Model):
    # Atributos de la clase Request: status, description

    # Tipos de género
    PENDING = 'Pendiente'
    ACCEPTED = 'Aceptada'
    DENIED = 'Denegada'

    StatusType = (
        (PENDING, 'Pendiente'),
        (ACCEPTED, 'Aceptada'),
        (DENIED, 'Denegada'),
    )
    status = models.CharField(max_length=10, choices=StatusType, default=PENDING)
    description = models.CharField(max_length=200, help_text="Requerido. 200 carácteres como máximo")

    # Relacion con actor enviado
    # Relacion con actor que recibe

    def __str__(self):
        return str(self.status) + ' - ' + str(self.description)

    class Meta:
        verbose_name = "Petición"
        verbose_name_plural = "Peticiones"


class RequestAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('status', 'description')
