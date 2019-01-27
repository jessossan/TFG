from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
import MYmessages
from MYmessages.forms import CreateMessageForm
from MYmessages.models import Message
from actors.models import Actor

# CREAR UN MENSAJE DESDE MENSAJES RECIBIDOS
@login_required(login_url='/login/')
def create_message_received(request):
    """
	Creación del mensaje desde la vista de recibidos.
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

            # Controlar que no se envie mensaje a sí mismo
            if recipient == actor:
                return HttpResponseForbidden()

            # Mensaje para el que envia
            message = Message.objects.create(subject=subject, copy=False, text=text, sender=actor,
                                             recipient=recipient)

            # Mensaje para el que recibe (se duplica el mensaje para que no afecte al borrado)
            messageCopy = Message.objects.create(subject=subject, copy=True, text=text, sender=actor,
                                                 recipient=recipient)

            message.save()
            messageCopy.save()

            return HttpResponseRedirect('/messages/sent')

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

    return render(request, 'create_message_received.html', data)

# CREAR UN MENSAJE DESDE MENSAJES ENVIADOS
@login_required(login_url='/login/')
def create_message_sent(request):
    """
	Creación del mensaje desde la vista de enviados.
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

            # Controlar que no se envie mensaje a sí mismo
            if recipient == actor:
                return HttpResponseForbidden()

            # Mensaje para el que envia
            message = Message.objects.create(subject=subject, copy=False, text=text, sender=actor,
                                             recipient=recipient)

            # Mensaje para el que recibe (se duplica el mensaje para que no afecte al borrado)
            messageCopy = Message.objects.create(subject=subject, copy=True, text=text, sender=actor,
                                                 recipient=recipient)

            message.save()
            messageCopy.save()

            return HttpResponseRedirect('/messages/sent')

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

    return render(request, 'create_message_sent.html', data)


# LISTADO DE MENSAJES RECIBIDOS
def list_messages_received(request):

    # Recupera el actor
    actor = request.user.actor

    try:
        # Filtra por recibidos del actor y por copy = True
        messages_list_aux = Message.objects.all().filter(recipient=actor).filter(copy=True)

    except Exception as e:

        messages_list_aux = Message.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(messages_list_aux, 6)

    try:
        messages_list_aux = paginator.page(page)
    except PageNotAnInteger:
        messages_list_aux = paginator.page(1)
    except EmptyPage:
        messages_list_aux = paginator.page(paginator.num_pages)

    data = {
        'message_list': messages_list_aux,
        'title': 'Mensajes recibidos',
        # Para controlar el título de la vista
        'received': True,
    }
    return render(request, 'list_message.html', data)

# LISTADO DE MENSAJES ENVIADOS
def list_messages_sent(request):

    # Recupera el actor
    actor = request.user.actor

    try:
        # Filtra por recibidos del actor y por copy = True
        messages_list_aux = Message.objects.all().filter(sender=actor).filter(copy=False)

    except Exception as e:

        messages_list_aux = Message.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(messages_list_aux, 6)

    try:
        messages_list_aux = paginator.page(page)
    except PageNotAnInteger:
        messages_list_aux = paginator.page(1)
    except EmptyPage:
        messages_list_aux = paginator.page(paginator.num_pages)

    data = {
        'message_list': messages_list_aux,
        'title': 'Mensajes recibidos',
        # Para controlar el título de la vista
        'received': False,
    }
    return render(request, 'list_message.html', data)
