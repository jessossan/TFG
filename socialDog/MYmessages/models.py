from django.db import models
from django.contrib import admin


# Create your models here.


class Message(models.Model):
    # Atributos de la clase Message: creationDate, subject, text, copy
    creationDate = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=50, help_text="Requerido. 50 carácteres como máximo")
    text = models.CharField(max_length=200, help_text="Requerido. 200 carácteres como máximo")
    copy = models.BooleanField(default=False)

    #Relacion con actor enviado
    #Relacion con actor que recibe

    def __str__(self):
        return str(self.creationDate) + ' - ' + str(self.subject) + ' - ' + str(self.text) + ' - ' + str(self.copy)

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"


class MessageAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('creationDate', 'subject', 'text', 'copy')
