from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from MYmessages.forms import CreateMessageForm, ReplyMessageForm
from MYmessages.models import Message
from actors.models import Actor

# Create your views here.


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

# RESPONDER MENSAJE RECIBIDO
@login_required(login_url='/login/')
def reply_message_received(request, pk):
    """
	Responder mensaje recibido.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el actor
    actor = request.user.actor

    # Recupera el mensaje al que va a responder
    message_replied = get_object_or_404(Message, pk=pk)

    # Recupera el destinatario del mensaje
    recipient = get_object_or_404(Actor, pk=message_replied.sender.userAccount.pk)

    # Comprueba que ese mensaje lo ha recibido el actor
    if message_replied.recipient != actor:
        raise PermissionDenied

    # Comprobación de que no se responda a si mismo
    if recipient == actor:
        raise PermissionDenied

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = ReplyMessageForm(request.POST)
        if (form.is_valid()):
            # Crea el mensaje
            subject = form.cleaned_data["subject"]
            text = form.cleaned_data["text"]

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
        form = ReplyMessageForm()

        # Datos del modelo (vista)

    data = {
        'form': form,
        'title': 'Crea el mensaje',
        'year': datetime.now().year,
        'recipient': recipient,
        # Recuperar el asunto del mensaje contestado
        'subject': message_replied.subject,
    }

    return render(request, 'reply_message_received.html', data)

# RESPONDER MENSAJE ENVIADO
@login_required(login_url='/login/')
def reply_message_sent(request, pk):
    """
	Responder mensaje enviado.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el actor
    actor = request.user.actor

    # Recupera el mensaje al que va a responder
    message_sent = get_object_or_404(Message, pk=pk)

    # Recupera el destinatario del mensaje
    recipient = get_object_or_404(Actor, pk=message_sent.recipient.userAccount.pk)

    # Comprueba que ese mensaje lo ha enviado el actor logueado
    if message_sent.sender != actor:
        raise PermissionDenied

    # Comprobación de que no se responda a si mismo
    if recipient == actor:
        raise PermissionDenied

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = ReplyMessageForm(request.POST)
        if (form.is_valid()):
            # Crea el mensaje
            subject = form.cleaned_data["subject"]
            text = form.cleaned_data["text"]

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
        form = ReplyMessageForm()

        # Datos del modelo (vista)

    data = {
        'form': form,
        'title': 'Crea el mensaje',
        'year': datetime.now().year,
        'recipient': recipient,
        # Para poner el mismo asunto
        'subject': message_sent.subject,
    }

    return render(request, 'reply_message_sent.html', data)

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
@login_required(login_url='/login/')
def list_messages_received(request):

    # Recupera el actor
    actor = request.user.actor

    try:
        # Filtra por recibidos del actor y por copy = True
        messages_list_aux = Message.objects.all().filter(recipient=actor).filter(copy=True).order_by('-creationDate')

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
@login_required(login_url='/login/')
def list_messages_sent(request):

    # Recupera el actor
    actor = request.user.actor

    try:
        # Filtra por recibidos del actor y por copy = True
        messages_list_aux = Message.objects.all().filter(sender=actor).filter(copy=False).order_by('-creationDate')

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


# BORRAR MENSAJES RECIBIDOS
@login_required(login_url='/login/')
def delete_message_received(request, pk):
    messageReceived = get_object_or_404(Message, pk=pk)

    actor = request.user.actor

    # Comprueba que sea su mensaje y que es copia
    if messageReceived.recipient != actor or not messageReceived.copy:
        raise PermissionDenied

    if request.method == 'POST':
        messageReceived.delete()
        return HttpResponseRedirect('/messages/received')

    data = {
        'actor': actor,
        'message': messageReceived,
    }

    return render(request, 'delete_message_received.html', data)


# BORRAR MENSAJES ENVIADOS
@login_required(login_url='/login/')
def delete_message_sent(request, pk):
    messageSent = get_object_or_404(Message, pk=pk)

    actor = request.user.actor

    # Comprueba que sea su mensaje y que es copia
    if messageSent.sender != actor or messageSent.copy:
        raise PermissionDenied

    if request.method == 'POST':
        messageSent.delete()
        return HttpResponseRedirect('/messages/sent')

    data = {
        'actor': actor,
        'message': messageSent,
    }

    return render(request, 'delete_message_sent.html', data)