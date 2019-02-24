from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class CreateRateForm(forms.Form):
    """Formulario de creación de valoración"""

    # Campos requeridos por la valoración

    stars = forms.IntegerField(required=False, validators=[MinValueValidator(0), MaxValueValidator(5)], label='Estrellas')
    description = forms.CharField(max_length=200, label='Descripción')


class EditRateForm(forms.Form):
    """Formulario de edición de valoración"""

    # Campos requeridos por el comentario

    stars = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], label='Estrellas')
    description = forms.CharField(max_length=200, label='Descripción')