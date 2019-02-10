from django import forms

from MYrequests.models import Request
from actors.models import Actor


class CreateRequestForm(forms.Form):
    """Formulario creación de la solicitud de amistad"""

    # Campos requeridos por la Request

    description = forms.CharField(max_length=200, label='Descripción')
    followed = forms.ModelChoiceField(queryset=Actor.objects.all(), empty_label=None, label='Seguido')

    # Recuperamos el usuario que esta realizando la operación
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreateRequestForm, self).__init__(*args, **kwargs)

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Recuperamos el actor que esta realizando la operación
            actor = Actor.objects.get(userAccount_id=self.user.id)

            # Recuperamos el actor al que está intentando seguir
            followed = self.cleaned_data["followed"]

            # Recupera todas las peticiones pendientes que ha enviado el actor(seguidor)
            actorFollower = Request.objects.filter(follower=actor, copy=False, status='Pendiente')

            # Recupera todas las peticiones aceptadas que ha enviado el actor(seguidor)
            actorFollower = actorFollower | Request.objects.filter(follower=actor, copy=False, status='Aceptada')

            # Recupera todas las peticiones pendientes que ha recibido el actor
            actorFollowed = Request.objects.filter(followed=actor, copy=False, status='Pendiente')

            # Recupera todas las peticiones aceptadas que ha recibido el actor
            actorFollowed = actorFollowed | Request.objects.filter(followed=actor, copy=False, status='Aceptada')

            # Comprueba si el actor logueado ha enviado una peticion ya a ese followed
            for requestSent in actorFollower:
                if requestSent.followed == followed:
                    raise forms.ValidationError(
                        "Ya ha enviado una solicitud a esa persona, compruebe sus solicitudes enviadas")

            # Comprueba si el actor loguaedo ha recibido ya una petición de ese followed
            for requestSent in actorFollowed:
                if requestSent.follower == followed:
                    raise forms.ValidationError(
                        "Ya existe una solicitud entre ambos, compruebe sus solicitudes recibidas")


class SendRequestForm(forms.Form):
    """Formulario envío de solicitud de amistad"""

    # Campos requeridos por la Request

    description = forms.CharField(max_length=200, label='Descripción')
