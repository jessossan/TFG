"""
Definition of forms.
"""
# encoding:utf-8
from django import forms
from actors.models import validate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


# LOGIN


class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesión"""
    username = forms.CharField(max_length=254, widget=forms.TextInput(
        {'class': 'form-control', 'required': True, 'autofocus': True, 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(label=_("Contraseña"), widget=forms.PasswordInput(
        {'class': 'form-control', 'required': True, 'placeholder': 'Contraseña'}))


# REGISTROS

class RegisterCustomerForm(forms.Form):
    """Formulario registro como Usuario"""

    # Campos requeridos por el User model
    username = forms.CharField(min_length=5, max_length=32, label='Nombre de usuario')
    password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                       label='Confirmar contraseña')
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Campos requeridos por el modelo Actor-Usuario
    phone = forms.CharField(max_length=11, validators=[RegexValidator(regex=r'^(\d{9})$',
                                                                      message='El teléfono debe estar compuesto de 9 dígitos.')],
                            label='Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$',
                                                                   message='El D.N.I. debe estar compuesto de 8 dígitos seguidos de 1 letra mayúscula.')],
                          label='D.N.I.')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida que el username no sea repetido
            username = self.cleaned_data["username"]
            num_usuarios = User.objects.filter(username=username).count()
            if (num_usuarios > 0):
                raise forms.ValidationError(
                    "El nombre de usuario ya está ocupado. Por favor, eliga otro para completar su registro.")

            dni = self.cleaned_data["dni"]
            try:
                validate(dni)
            except Exception as e:
                raise forms.ValidationError("El formato del DNI no es correcto")

            # Valida que la contraseña se haya confirmado correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                raise forms.ValidationError(
                    "Las contraseñas introducidas no coinciden. Por favor, asegúrese de confirmarla correctamente.")
