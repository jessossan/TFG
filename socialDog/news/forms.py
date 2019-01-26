from django import forms

# CRIADOR
class CreateBreederNewsForm(forms.Form):
    """Formulario registro de una noticia del criador"""

    # Campos requeridos por la Noticia

    title = forms.CharField(max_length=25, label='Nombre')
    description = forms.CharField(max_length=200, label='Descripción')
    photo = forms.ImageField(required=False, label='Foto')


class EditNewsForm(forms.Form):
    """Formulario de edición de una noticia del criador o de la asociacion"""

    # Campos requeridos por la noticia

    title = forms.CharField(max_length=50, label='Título')
    description = forms.CharField(max_length=200, label='Descripción')
    photo = forms.ImageField(required=False, label='Foto')


# ASOCIACION

class CreateAssociationNewsForm(forms.Form):
    """Formulario registro de un evento de la asociacion"""

    # Campos requeridos por la noticia

    title = forms.CharField(max_length=50, label='Título')
    description = forms.CharField(max_length=200, label='Descripción')
    photo = forms.ImageField(required=False, label='Foto de la noticia')

