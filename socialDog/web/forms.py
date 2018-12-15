"""
Definition of forms.
"""
# encoding:utf-8
from django import forms
from actors.models import validate, Breeder, Association
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

# LOGIN
from breeds.models import Breed
from provinces.models import Province


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


class RegisterAssociationForm(forms.Form):
    """Formulario registro como Asociación"""

    # Campos requeridos por el User model
    username = forms.CharField(min_length=5, max_length=32, label='Nombre de usuario')
    password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                       label='Confirmar contraseña')
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Campos requeridos por el modelo Actor-Asociación
    phone = forms.CharField(max_length=11, validators=[RegexValidator(regex=r'^(\d{9})$',
                                                                      message='El teléfono debe estar compuesto de 9 dígitos.')],
                            label='Teléfono')
    photo = forms.ImageField(required=False)
    centerName = forms.CharField(max_length=50, label="Nombre del centro")
    postalCode = forms.CharField(max_length=5, validators=[RegexValidator(regex=r'^(\d{5})$',
                                                                      message='El código postal debe estar compuesto por 5 dígitos.'),], label='Código Postal')
    province = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label=None, label='Provincia')
    address = forms.CharField(max_length=50, label='Dirección')
    opening = forms.TimeField(label='Hora de apertura')
    closing = forms.TimeField(label='Hora de cierre')
    cif = forms.CharField(max_length=9,
                          validators=[RegexValidator(regex=r'^([G]{1})(\d{8})$',
                                                     message='El código de identificación debe estar compuesto de 9 dígitos.')],
                          label="C.I.F.")
    private = forms.BooleanField(label='Perfil privado',required=False)

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

            # Valida que la contraseña se haya confirmado correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                raise forms.ValidationError(
                    "Las contraseñas introducidas no coinciden. Por favor, asegúrese de confirmarla correctamente.")

            # Valida que el centro esta ya en uso por una Asociacion
            centerName = self.cleaned_data["centerName"]
            num_asociaciones_mismo_centro = Association.objects.filter(centerName=centerName).count()
            if (num_asociaciones_mismo_centro > 0):
                raise forms.ValidationError(
                    "El nombre del centro ya está en uso. Por favor, eliga otro para completar su registro.")


            # Valida que el centro esta ya en uso por un Criador
            centerName = self.cleaned_data["centerName"]
            num_criadores_mismo_centro = Breeder.objects.filter(centerName=centerName).count()
            if (num_criadores_mismo_centro > 0):
                raise forms.ValidationError(
                    "El nombre del centro ya está en uso. Por favor, eliga otro para completar su registro.")

            # Valida que el cif esta ya en uso por una Asociacion
            cif = self.cleaned_data["cif"]
            num_mismos_cif = Association.objects.filter(cif=cif).count()
            if (num_mismos_cif > 0):
                raise forms.ValidationError(
                    "El C.I.F ya está en uso. Por favor, revise su C.I.F")

class RegisterBreederForm(forms.Form):
    """Formulario registro como Criador"""

    # Campos requeridos por el User model
    username = forms.CharField(min_length=5, max_length=32, label='Nombre de usuario')
    password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                       label='Confirmar contraseña')
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Campos requeridos por el modelo Actor-Breeder
    phone = forms.CharField(max_length=11, validators=[RegexValidator(regex=r'^(\d{9})$',
                                                                      message='El teléfono debe estar compuesto de 9 dígitos.')],
                            label='Teléfono')
    photo = forms.ImageField(required=False)
    centerName = forms.CharField(max_length=50, label="Nombre del centro")
    postalCode = forms.CharField(max_length=5, validators=[RegexValidator(regex=r'^(\d{5})$',
                                                                      message='El código postal debe estar compuesto por 5 dígitos.')], label='Código Postal')
    province = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label=None, label='Provincia')
    address = forms.CharField(max_length=50, label='Dirección')
    opening = forms.TimeField(label='Hora de apertura')
    closing = forms.TimeField(label='Hora de cierre')
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$',
                                                                   message='El D.N.I. debe estar compuesto de 8 dígitos seguidos de 1 letra mayúscula.')],
                          label='D.N.I.')
    private = forms.BooleanField(label='Perfil privado',required=False)
    breeds = forms.ModelMultipleChoiceField(queryset=Breed.objects.all(), widget=forms.CheckboxSelectMultiple, label='Razas')

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

            # Valida que el centro esta ya en uso por una Asociacion
            centerName = self.cleaned_data["centerName"]
            num_asociaciones_mismo_centro = Association.objects.filter(centerName=centerName).count()
            if (num_asociaciones_mismo_centro > 0):
                raise forms.ValidationError(
                    "El nombre del centro ya está en uso. Por favor, eliga otro para completar su registro.")

            # Valida que el centro esta ya en uso por un Criador
            centerName = self.cleaned_data["centerName"]
            num_criadores_mismo_centro = Breeder.objects.filter(centerName=centerName).count()
            if (num_criadores_mismo_centro > 0):
                raise forms.ValidationError(
                    "El nombre del centro ya está en uso. Por favor, eliga otro para completar su registro.")
