from django import forms
from django.core.validators import MinValueValidator

from MYrequests.models import Request
from actors.models import Actor


class CreateMessageForm(forms.Form):
    """Formulario creación del mensaje"""

    # Campos requeridos por el Message

    subject = forms.CharField(max_length=50, label='Asunto')
    text = forms.CharField(max_length=200, label='Texto')
    recipient = forms.ModelChoiceField(queryset=Actor.objects.all(), empty_label=None, label='Usuario')

    # Recuperamos el usuario que esta realizando la operación
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreateMessageForm, self).__init__(*args, **kwargs)

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Recuperamos el actor que esta realizando la operación
            actor = Actor.objects.get(userAccount_id=self.user.id)

            # Recuperamos el destinatario del mensaje
            recipient = self.cleaned_data["recipient"]

            acceptedStatus = Request.StatusType[1][0]

            # Recupera todas las peticiones que ha enviado el actor y estan aceptadas
            requestFollowers = Request.objects.filter(follower=actor, copy=False, status=acceptedStatus)

            actors = Actor.objects.none()
            actorsFollower = Actor.objects.none()
            actorsFollowed = Actor.objects.none()

            # Recupera los actores de las solicitudes enviadas aceptadas
            for reqFollower in requestFollowers:
                actorsFollower = actorsFollower | Actor.objects.all().filter(pk=reqFollower.followed.pk)

            # Recupera todas las peticiones que ha recibido el actor y estan aceptadas
            requestFolloweds = Request.objects.filter(followed=actor, copy=False, status=acceptedStatus)

            # Recupera los actores de las solicitudes recibidas aceptadas
            for reqFollowed in requestFolloweds:
                actorsFollowed = actorsFollowed | Actor.objects.all().filter(pk=reqFollowed.follower.pk)

            # Lista de amigos del actor logueado
            actors = actorsFollower | actorsFollowed

            isFriend = False

            # Recorre la lista de amigos
            for friend in actors:
                # Si el destinatario esta en su lista de amigos
                if friend == recipient:
                    isFriend = True

            # Si el destinatario no está en la lista de amigos
            if (not isFriend):
                raise forms.ValidationError(
                    "Ya no son amigos, recargue la página o compruebe su lista de amigos")


class ReplyMessageForm(forms.Form):
    """Formulario respuesta del mensaje"""

    # Campos requeridos por el Message

    subject = forms.CharField(max_length=50, label='Asunto')
    text = forms.CharField(max_length=200, label='Texto')
