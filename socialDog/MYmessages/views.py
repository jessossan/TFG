from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
import MYmessages
from MYmessages.forms import CreateMessageForm
from MYmessages.models import Message
from actors.models import Actor


@login_required(login_url='/login/')
def create_message(request):
    """
	Creación del mensaje.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el actor
    actor = request.user.actor

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = CreateMessageForm(request.POST)
        if (form.is_valid()):
            # Crea el mensaje
            subject = form.cleaned_data["subject"]
            text = form.cleaned_data["text"]
            recipient = form.cleaned_data["recipient"]

            # Mensaje para el que envia
            message = Message.objects.create(subject=subject, copy=False, text=text, sender=actor,
                                             recipient=recipient)

            # Mensaje para el que recibe (se duplica el mensaje para que no afecte al borrado)
            messageCopy = Message.objects.create(subject=subject, copy=True, text=text, sender=actor,
                                                 recipient=recipient)

            message.save()
            messageCopy.save()

            return HttpResponseRedirect('/MYmessages')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = CreateMessageForm()

        # Datos del modelo (vista)

    # Excluye al actor que esta creando el mensaje # FALTA FILTRAR POR AMIGOS
    actors = Actor.objects.all().exclude(pk=actor.pk)
    data = {
        'form': form,
        'title': 'Crea el mensaje',
        'year': datetime.now().year,
        'actors': actors,
    }

    return render(request, 'create_message.html', data)
