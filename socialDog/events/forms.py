from django import forms
from django.core.validators import MinValueValidator

from breeds.models import Breed
from dogs.models import Dog


class CreateBreederEventForm(forms.Form):
    """Formulario registro de un evento del criador"""

    # Campos requeridos por el Evento

    title = forms.CharField(max_length=50, label='Nombre')
    description = forms.CharField(max_length=200, label='Descripción')
    place = forms.CharField(max_length=50, label='Lugar')
    startDate = forms.DateField(label='Fecha de inicio')
    startTime = forms.TimeField(label='Hora de inicio')

    finishDate = forms.DateField(label='Fecha de fin')
    finishTime = forms.TimeField(label='Hora de fin')

    length = forms.TimeField(required=False, label='Duración')


class EditEventForm(forms.Form):
    """Formulario de edición de un evento del criador o de la asociacion"""

    # Campos requeridos por el Evento

    title = forms.CharField(max_length=50, label='Nombre')
    description = forms.CharField(max_length=200, label='Descripción')
    place = forms.CharField(max_length=50, label='Lugar')
    startDate = forms.DateField(label='Fecha de inicio')
    startTime = forms.TimeField(label='Hora de inicio')

    finishDate = forms.DateField(label='Fecha de fin')
    finishTime = forms.TimeField(label='Hora de fin')

    length = forms.TimeField(required=False, label='Duración')
