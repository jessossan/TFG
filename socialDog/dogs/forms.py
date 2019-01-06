from django import forms
from django.core.validators import MinValueValidator

from breeds.models import Breed
from dogs.models import Dog


class RegisterDogForm(forms.Form):
    """Formulario registro de un perro"""

    # Campos requeridos por el Dog

    name = forms.CharField(max_length=50, label='Nombre')
    age = forms.IntegerField(validators=[MinValueValidator(0)], label='Edad')
    gender = forms.ChoiceField(choices=Dog.GenderType, label='Género')
    descendant = forms.CharField(max_length=200, required=False, label='Descendencia')
    details = forms.CharField(max_length=200, required=False, label='Detalles')
    photo = forms.ImageField(required=False, label='Foto del perro')
    awards = forms.CharField(max_length=200, help_text="Premios, no requerido", required=False)
    breed = forms.ModelChoiceField(queryset = Breed.objects.all(), empty_label = None, label = 'Raza')

