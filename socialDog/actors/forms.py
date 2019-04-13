from django import forms
from django.core.validators import RegexValidator
from actors.models import validate, Association, Breeder
from django.contrib.auth.models import User

from breeds.models import Breed
from provinces.models import Province

"""USUARIO"""  # USUARIO


class EditCustomerProfile(forms.Form):
    """Formulario registro como Usuario"""

    # Campos requeridos por el User model
    email = forms.EmailField(max_length=100)
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
    actual_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                      label='Contraseña actual')
    password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput, label='Nueva contraseña')
    confirm_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                       label='Confirmar nueva contraseña')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida la contraseña actual del usuario sea la que ha introducido en el formulario
            actual_password = self.cleaned_data["actual_password"]
            userAccountId = self.cleaned_data["userAccountId"]
            userAccount = User.objects.get(pk=userAccountId)
            if not (userAccount.check_password(actual_password)):
                raise forms.ValidationError(
                    "Por favor, introduzca correctamente su contraseña actual para realizar el cambio.")

            # Valida que la nueva contraseña haya sido confirmada correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                raise forms.ValidationError(
                    "La nueva contraseña no coincide. Por favor, asegúrese de confirmarla correctamente.")

            # Valida que la nueva contraseña no sea igual a la actual
            if (password == actual_password):
                raise forms.ValidationError(
                    "La nueva contraseña no puede ser similar a la actual. Por favor, elija otra.")


"""CRIADOR"""  # CRIADOR


class EditBreederProfile(forms.Form):
    """ Formulario de edición del perfil Breeder """

    # Campos editables del User model
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Campos requeridos por el modelo Actor-Breeder
    phone = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^(\d{9})$',
                                                                     message='El teléfono debe estar compuesto de 9 dígitos.')],
                            label='Teléfono')
    photo = forms.ImageField(required=False)
    cif = forms.CharField(max_length=9,
                          validators=[RegexValidator(regex=r'^([G]{1})(\d{8})$',
                                                     message='El código de identificación fiscal debe comenzar con G seguido de 8 dígitos.')],
                          label="C.I.F.")
    opening = forms.TimeField(label='Hora de apertura')
    closing = forms.TimeField(label='Hora de cierre')
    address = forms.CharField(max_length=50, label='Dirección')
    private = forms.BooleanField(label='Perfil privado', required=False)
    postalCode = forms.CharField(max_length=5, validators=[RegexValidator(regex=r'^(\d{5})$',
                                                                          message='El código postal debe estar compuesto por 5 dígitos.'), ],
                                 label='Código Postal')
    centerName = forms.CharField(max_length=50, label="Nombre del centro")
    notes = forms.CharField(max_length=200, required=False, label="Observaciones sobre el horario")
    province = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label=None, label='Provincia')
    breeds = forms.ModelMultipleChoiceField(queryset=Breed.objects.all(), widget=forms.CheckboxSelectMultiple,
                                            label='Razas')

    # Recuperamos el usuario que esta realizando la operación
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditBreederProfile, self).__init__(*args, **kwargs)

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:
            # Recuperamos el criador que esta realizando la operación
            breeder = Breeder.objects.get(userAccount_id=self.user.id)

            # Recuperamos el nombre del centro y cif del criador que esta modificando el perfil
            ownCenterName = breeder.centerName
            ownCif = breeder.cif

            # Valida que el centro esta ya en uso por una Asociacion
            centerName = self.cleaned_data["centerName"]
            num_asociaciones_mismo_centro = Association.objects.filter(centerName=centerName).count()
            if (num_asociaciones_mismo_centro > 0):
                raise forms.ValidationError(
                    "El nombre del centro ya está en uso. Por favor, eliga otro para completar su registro.")

            # Valida que el centro esta ya en uso por un Criador
            centerName = self.cleaned_data["centerName"]
            # Excluye de la lista su propio nombre del centro
            num_criadores_mismo_centro = Breeder.objects.filter(centerName=centerName).exclude(
                centerName=ownCenterName).count()
            if (num_criadores_mismo_centro > 0):
                raise forms.ValidationError(
                    "El nombre del centro ya está en uso. Por favor, eliga otro para completar su registro.")

            # Valida que el cif esta ya en uso por un Criador
            cif = self.cleaned_data["cif"]
            # Excluye de la lista su propio cif
            num_mismos_cif = Breeder.objects.filter(cif=cif).exclude(cif=ownCif).count()
            if (num_mismos_cif > 0):
                raise forms.ValidationError(
                    "El C.I.F ya está en uso. Por favor, revise su C.I.F")

            # Valida que el cif esta ya en uso por un Asociación
            cif = self.cleaned_data["cif"]
            num_mismos_cif = Association.objects.filter(cif=cif).count()
            if (num_mismos_cif > 0):
                raise forms.ValidationError(
                    "El C.I.F ya está en uso. Por favor, revise su C.I.F")


class EditBreederPass(forms.Form):
    """ Formulario de edición de las contraseñas del criador """
    userAccountId = forms.IntegerField()
    actual_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                      label='Contraseña actual')
    password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput, label='Nueva contraseña')
    confirm_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                       label='Confirmar nueva contraseña')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida la contraseña actual del usuario sea la que ha introducido en el formulario
            actual_password = self.cleaned_data["actual_password"]
            userAccountId = self.cleaned_data["userAccountId"]
            userAccount = User.objects.get(pk=userAccountId)
            if not (userAccount.check_password(actual_password)):
                raise forms.ValidationError(
                    "Por favor, introduzca correctamente su contraseña actual para realizar el cambio.")

            # Valida que la nueva contraseña haya sido confirmada correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                raise forms.ValidationError(
                    "La nueva contraseña no coincide. Por favor, asegúrese de confirmarla correctamente.")

            # Valida que la nueva contraseña no sea igual a la actual
            if (password == actual_password):
                raise forms.ValidationError(
                    "La nueva contraseña no puede ser similar a la actual. Por favor, elija otra.")


"""ASOCIACION"""  # ASOCIACION


class EditAssociationProfile(forms.Form):
    """ Formulario de edición del perfil Association """

    # Campos editables del User model
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Campos requeridos por el modelo Actor-Association
    phone = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^(\d{9})$',
                                                                     message='El teléfono debe estar compuesto de 9 dígitos.')],
                            label='Teléfono')
    photo = forms.ImageField(required=False)
    cif = forms.CharField(max_length=9,
                          validators=[RegexValidator(regex=r'^([G]{1})(\d{8})$',
                                                     message='El código de identificación fiscal debe comenzar con G seguido de 8 dígitos.')],
                          label="C.I.F.")
    opening = forms.TimeField(label='Hora de apertura')
    closing = forms.TimeField(label='Hora de cierre')
    address = forms.CharField(max_length=50, label='Dirección')
    private = forms.BooleanField(label='Perfil privado', required=False)
    postalCode = forms.CharField(max_length=5, validators=[RegexValidator(regex=r'^(\d{5})$',
                                                                          message='El código postal debe estar compuesto por 5 dígitos.'), ],
                                 label='Código Postal')
    centerName = forms.CharField(max_length=50, label="Nombre del centro")
    notes = forms.CharField(max_length=200, required=False, label="Observaciones sobre el horario")
    province = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label=None, label='Provincia')

    # Recuperamos el usuario que esta realizando la operación
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditAssociationProfile, self).__init__(*args, **kwargs)

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:
            # Recuperamos la asociación que esta realizando la operación
            association = Association.objects.get(userAccount_id=self.user.id)

            # Recuperamos el nombre del centro y cif del criador que esta modificando el perfil
            ownCenterName = association.centerName
            ownCif = association.cif

            # Valida que el centro esta ya en uso por una Asociacion
            centerName = self.cleaned_data["centerName"]
            num_asociaciones_mismo_centro = Association.objects.filter(centerName=centerName).exclude(
                centerName=ownCenterName).count()
            if (num_asociaciones_mismo_centro > 0):
                raise forms.ValidationError(
                    "El nombre del centro ya está en uso. Por favor, eliga otro para completar su registro.")

            # Valida que el centro esta ya en uso por un Criador
            centerName = self.cleaned_data["centerName"]
            # Excluye de la lista su propio nombre del centro
            num_criadores_mismo_centro = Breeder.objects.filter(centerName=centerName).count()
            if (num_criadores_mismo_centro > 0):
                raise forms.ValidationError(
                    "El nombre del centro ya está en uso. Por favor, eliga otro para completar su registro.")

            # Valida que el cif esta ya en uso por un Criador
            cif = self.cleaned_data["cif"]
            # Excluye de la lista su propio cif
            num_mismos_cif = Breeder.objects.filter(cif=cif).count()
            if (num_mismos_cif > 0):
                raise forms.ValidationError(
                    "El C.I.F ya está en uso. Por favor, revise su C.I.F")

            # Valida que el cif esta ya en uso por un Asociación
            cif = self.cleaned_data["cif"]
            num_mismos_cif = Association.objects.filter(cif=cif).exclude(cif=ownCif).count()
            if (num_mismos_cif > 0):
                raise forms.ValidationError(
                    "El C.I.F ya está en uso. Por favor, revise su C.I.F")


class EditAssociationPass(forms.Form):
    """ Formulario de edición de las contraseñas del association """
    userAccountId = forms.IntegerField()
    actual_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                      label='Contraseña actual')
    password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput, label='Nueva contraseña')
    confirm_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                       label='Confirmar nueva contraseña')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida la contraseña actual del usuario sea la que ha introducido en el formulario
            actual_password = self.cleaned_data["actual_password"]
            userAccountId = self.cleaned_data["userAccountId"]
            userAccount = User.objects.get(pk=userAccountId)
            if not (userAccount.check_password(actual_password)):
                raise forms.ValidationError(
                    "Por favor, introduzca correctamente su contraseña actual para realizar el cambio.")

            # Valida que la nueva contraseña haya sido confirmada correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                raise forms.ValidationError(
                    "La nueva contraseña no coincide. Por favor, asegúrese de confirmarla correctamente.")

            # Valida que la nueva contraseña no sea igual a la actual
            if (password == actual_password):
                raise forms.ValidationError(
                    "La nueva contraseña no puede ser similar a la actual. Por favor, elija otra.")
