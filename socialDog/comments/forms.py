from django import forms

from MYrequests.models import Request
from actors.models import Actor


class CreateCommentForm(forms.Form):
    """Formulario de creación de comentario"""

    # Campos requeridos por el comentario

    text = forms.CharField(max_length=200, label='Texto')



class EditCommentForm(forms.Form):
    """Formulario de edición de comentario"""

    # Campos requeridos por el comentario

    text = forms.CharField(max_length=200, label='Texto')