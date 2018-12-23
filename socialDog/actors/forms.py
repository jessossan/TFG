from django import forms
from django.core.validators import RegexValidator
from actors.models import validate
from django.contrib.auth.models import User

from breeds.models import Breed
from provinces.models import Province

"""USUARIO""" # USUARIO

class EditCustomerProfile(forms.Form):
    """Formulario registro como Usuario"""

    # Campos requeridos por el User model
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

            dni = self.cleaned_data["dni"]
            try:
                validate(dni)
            except Exception as e:
                raise forms.ValidationError("El formato del DNI no es correcto")

class EditCustomerPass(forms.Form):
    """ Formulario de edición de las contraseñas del usuario """
    userAccountId = forms.IntegerField()
    actual_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Contraseña actual')
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Nueva contraseña')
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Confirmar nueva contraseña')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida la contraseña actual del usuario sea la que ha introducido en el formulario
            actual_password = self.cleaned_data["actual_password"]
            userAccountId = self.cleaned_data["userAccountId"]
            userAccount = User.objects.get(pk = userAccountId)
            if not (userAccount.check_password(actual_password)):
                    raise forms.ValidationError("Por favor, introduzca correctamente su contraseña actual para realizar el cambio.")

            # Valida que la nueva contraseña haya sido confirmada correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                    raise forms.ValidationError("La nueva contraseña no coincide. Por favor, asegúrese de confirmarla correctamente.")

            # Valida que la nueva contraseña no sea igual a la actual
            if (password == actual_password):
                raise forms.ValidationError("La nueva contraseña no puede ser similar a la actual. Por favor, elija otra.")



"""CRIADOR""" # CRIADOR

class EditBreederProfile(forms.Form):
    """ Formulario de edición del perfil Breeder """

    # Campos editables del User model
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    # Campos requeridos por el modelo Actor-Breeder
    phone = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
    photo = forms.ImageField(required = False)
    cif = forms.CharField(max_length=9,
                          validators=[RegexValidator(regex=r'^([G]{1})(\d{8})$',
                                                     message='El código de identificación fiscal debe estar compuesto de 9 dígitos.')],
                          label="C.I.F.")
    opening = forms.TimeField(label='Hora de apertura')
    closing = forms.TimeField(label='Hora de cierre')
    address = forms.CharField(max_length=50, label='Dirección')
    private = forms.BooleanField(label='Perfil privado', required=False)
    postalCode = forms.CharField(max_length=5, validators=[RegexValidator(regex=r'^(\d{5})$',
                                                                          message='El código postal debe estar compuesto por 5 dígitos.'), ],
                                 label='Código Postal')
    centerName = forms.CharField(max_length=50, label="Nombre del centro")
    province = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label=None, label='Provincia')


class EditBreederPass(forms.Form):
    """ Formulario de edición de las contraseñas del criador """
    userAccountId = forms.IntegerField()
    actual_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Contraseña actual')
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Nueva contraseña')
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Confirmar nueva contraseña')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida la contraseña actual del usuario sea la que ha introducido en el formulario
            actual_password = self.cleaned_data["actual_password"]
            userAccountId = self.cleaned_data["userAccountId"]
            userAccount = User.objects.get(pk = userAccountId)
            if not (userAccount.check_password(actual_password)):
                    raise forms.ValidationError("Por favor, introduzca correctamente su contraseña actual para realizar el cambio.")

            # Valida que la nueva contraseña haya sido confirmada correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                    raise forms.ValidationError("La nueva contraseña no coincide. Por favor, asegúrese de confirmarla correctamente.")

            # Valida que la nueva contraseña no sea igual a la actual
            if (password == actual_password):
                raise forms.ValidationError("La nueva contraseña no puede ser similar a la actual. Por favor, elija otra.")


"""ASOCIACION""" # ASOCIACION

class EditAssociationProfile(forms.Form):
    """ Formulario de edición del perfil Association """

    # Campos editables del User model
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    # Campos requeridos por el modelo Actor-Association
    phone = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
    photo = forms.ImageField(required = False)
    cif = forms.CharField(max_length=9,
                          validators=[RegexValidator(regex=r'^([G]{1})(\d{8})$',
                                                     message='El código de identificación fiscal debe estar compuesto de 9 dígitos.')],
                          label="C.I.F.")
    opening = forms.TimeField(label='Hora de apertura')
    closing = forms.TimeField(label='Hora de cierre')
    address = forms.CharField(max_length=50, label='Dirección')
    private = forms.BooleanField(label='Perfil privado', required=False)
    postalCode = forms.CharField(max_length=5, validators=[RegexValidator(regex=r'^(\d{5})$',
                                                                          message='El código postal debe estar compuesto por 5 dígitos.'), ],
                                 label='Código Postal')
    centerName = forms.CharField(max_length=50, label="Nombre del centro")
    province = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label=None, label='Provincia')


class EditAssociationPass(forms.Form):
    """ Formulario de edición de las contraseñas del association """
    userAccountId = forms.IntegerField()
    actual_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Contraseña actual')
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Nueva contraseña')
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Confirmar nueva contraseña')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida la contraseña actual del usuario sea la que ha introducido en el formulario
            actual_password = self.cleaned_data["actual_password"]
            userAccountId = self.cleaned_data["userAccountId"]
            userAccount = User.objects.get(pk = userAccountId)
            if not (userAccount.check_password(actual_password)):
                    raise forms.ValidationError("Por favor, introduzca correctamente su contraseña actual para realizar el cambio.")

            # Valida que la nueva contraseña haya sido confirmada correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                    raise forms.ValidationError("La nueva contraseña no coincide. Por favor, asegúrese de confirmarla correctamente.")

            # Valida que la nueva contraseña no sea igual a la actual
            if (password == actual_password):
                raise forms.ValidationError("La nueva contraseña no puede ser similar a la actual. Por favor, elija otra.")