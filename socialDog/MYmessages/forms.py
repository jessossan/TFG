from django import forms
from django.core.validators import MinValueValidator

from actors.models import Actor


class CreateMessageForm(forms.Form):
    """Formulario creación del mensaje"""

    # Campos requeridos por el Message

    subject = forms.CharField(max_length=50, label='Asunto')
    text = forms.CharField(max_length=200, label='Texto')
    recipient = forms.ModelChoiceField(queryset=Actor.objects.all(), empty_label=None, label='Usuario')


class ReplyMessageForm(forms.Form):
    """Formulario respuesta del mensaje"""

    # Campos requeridos por el Message

    subject = forms.CharField(max_length=50, label='Asunto')
    text = forms.CharField(max_length=200, label='Texto')
