from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib import admin
from stdnum.exceptions import *
from stdnum.util import clean


# Create your models here.
from breeds.models import Breed
from provinces.models import Province


class Actor(models.Model):
    """
    Clase que define el modelo Actor: nombre, aepllidos, teléfono, foto.
    """
    phone = models.CharField(max_length=9, help_text='Requerido. Patrón de 9 dígitos.',
                             validators=[
                                 RegexValidator(regex=r'^(\d{9})$', message='El formato introducido es incorrecto.')])
    photo = models.ImageField(null=True, blank=True, upload_to='uploads/')
    people = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    # Relaciones
    userAccount = models.OneToOneField('auth.User', verbose_name='User Account', on_delete=models.CASCADE,
                                       primary_key=True)

    # Relación peticion
    # Relación valoracion
    # Relación mensaje
    # Relación likedislike
    # Relación comentario

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'  # Falta people

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actores"


class ActorAdminPanel(admin.ModelAdmin):
    """
    Clase que oculta el modelo Actor en el panel de administración.
    """

    def get_model_perms(self, request):
        return {}


class Administrator(Actor):
    """
    Clase que define el modelo Administrador: dni
    """
    dni = models.CharField(verbose_name='D.N.I.', max_length=9,
                           help_text='Requerido. 8 dígitos y una letra.',
                           validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$',
                                                      message='El formato introducido es incorrecto.')])

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"


class AdministratorAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Administrador que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'dni')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


class Customer(Actor):
    """
    Clase que define el modelo Usuario: dni
    """
    dni = models.CharField(verbose_name='D.N.I.', max_length=9,
                           help_text='Requerido. 8 dígitos y una letra.',
                           validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$',
                                                      message='El formato introducido es incorrecto.')])

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    def full_clean(self, exclude=None, validate_unique=True):
        if not validate(self.dni):
            raise ValidationError({
                NON_FIELD_ERRORS: ['El DNI tiene un formato incorrecto', ],
            })

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class CustomerAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Usuario que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'dni', 'people')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


class Association(Actor):
    """
    Clase que define el modelo Asociación: centerName, address, postalCode, cif, opening, closing, province, private
    """
    centerName = models.CharField(max_length=50, unique=True, help_text='Requerido. 50 carácteres como máximo.')
    address = models.CharField(max_length=50, help_text='Requerido. 50 carácteres como máximo.')
    postalCode = models.CharField(verbose_name='Código postal', max_length=5,
                                  help_text='Requerido. 5 dígitos como máximo.',
                                  validators=[RegexValidator(regex=r'^(\d{5})$',
                                                             message='El formato introducido es incorrecto.')])
    cif = models.CharField(verbose_name='CIF or Center Code', max_length=9,
                                        validators=[RegexValidator(regex=r'^([G]{1})(\d{8})$',
                                                                                        message='El código de identificación debe estar compuesto de 9 dígitos.')],
                                        unique=True,
                                        help_text='Requerido. CIF para asociaciones. Empieza por G, seguido de 8 dígitos')
    opening = models.TimeField()
    closing = models.TimeField()
    # Relación con provincia
    province = models.ForeignKey(Province, on_delete = models.SET_NULL, null = True)
    private = models.BooleanField(default=True)

    def __str__(self):
        return self.centerName + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name = "Asociación"
        verbose_name_plural = "Asociaciones"


class AssociationAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Actor-Asociación que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'people', 'centerName', 'address', 'cif', 'opening', 'closing')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


class Breeder(Actor):
    """
    Clase que define el modelo Criador: centerName, address, postalCode, dni, opening, closing, province, private
    """
    centerName = models.CharField(max_length=50, unique=True, help_text='Requerido. 50 carácteres como máximo.')
    address = models.CharField(max_length=50, help_text='Requerido. 50 carácteres como máximo.')
    postalCode = models.CharField(verbose_name='Postal Code', max_length=5,
                                  help_text='Requerido. 5 dígitos como máximo.',
                                  validators=[RegexValidator(regex=r'^(\d{5})$',
                                                             message='El formato introducido es incorrecto.')])
    dni = models.CharField(verbose_name='D.N.I.', max_length=9,
                           help_text='Requerido. 8 dígitos y una letra.',
                           validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$',
                                                      message='El formato introducido es incorrecto.')])
    opening = models.DateTimeField()
    closing = models.DateTimeField()
    private = models.BooleanField(default=True)

    # Relación con provincia
    province = models.ForeignKey(Province, on_delete = models.SET_NULL, null = True)
    # Relación con razas
    breeds = models.ManyToManyField(Breed)

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    def full_clean(self, exclude=None, validate_unique=True):
        if not validate(self.dni):
            raise ValidationError({
                NON_FIELD_ERRORS: ['El DNI tiene un formato incorrecto', ],
            })

    class Meta:
        verbose_name = "Criador"
        verbose_name_plural = "Criadores"


class BreederAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Criador que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'people', 'dni', 'centerName', 'address', 'postalCode', 'opening', 'closing')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


def validate(number):
    """Check if the number provided is a valid DNI number. This checks the
    length, formatting and check digit."""
    number = compact(number)
    if not number[:-1].isdigit():
        raise InvalidFormat()
    if len(number) != 9:
        raise InvalidLength()
    if calc_check_digit(number[:-1]) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number provided is a valid DNI number. This checks the
    length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    return 'TRWAGMYFPDXBNJZSQVHLCKE'[int(number) % 23]
