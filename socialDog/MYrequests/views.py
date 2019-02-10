from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from MYrequests.forms import CreateRequestForm, SendRequestForm
from MYrequests.models import Request
from actors.models import Actor


# LISTADO DE SOLICITUDES ENVIADAS

@login_required(login_url='/login/')
def list_requests_sent(request):
    # Recupera el actor logueado
    actor = request.user.actor

    try:
        # Ordenado por Aceptada, Denegada y Pendiente # Filtramos las que ha enviado el actor NO copia y NO borradas
        request_list_aux = Request.objects.all().filter(follower=actor, copy=False, deleted=False).order_by('status')

    except Exception as e:

        request_list_aux = Request.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(request_list_aux, 6)

    try:
        request_list_aux = paginator.page(page)
    except PageNotAnInteger:
        request_list_aux = paginator.page(1)
    except EmptyPage:
        request_list_aux = paginator.page(paginator.num_pages)

    data = {
        'request_list': request_list_aux,
        'title': 'Listado de solicitudes de amistad enviadas',
        # Controlar la vista para los botones
        'isSent': True,
    }
    return render(request, 'list_request_sent.html', data)


# LISTADO DE SOLICITUDES RECIBIDAS

@login_required(login_url='/login/')
def list_requests_received(request):
    # Recupera el actor logueado
    actor = request.user.actor

    try:
        # Ordenado por Pendiente, Denegada y Aceptada
        request_list_aux = Request.objects.all().filter(followed=actor).filter(copy=True).order_by('-status')

    except Exception as e:

        request_list_aux = Request.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(request_list_aux, 6)

    try:
        request_list_aux = paginator.page(page)
    except PageNotAnInteger:
        request_list_aux = paginator.page(1)
    except EmptyPage:
        request_list_aux = paginator.page(paginator.num_pages)

    data = {
        'request_list': request_list_aux,
        'title': 'Listado de solicitudes de amistad recibidas',
        # Controlar la vista para los botones
        'isSent': False,
    }
    return render(request, 'list_request_received.html', data)


# CREAR UNA SOLICITUD DE AMISTAD
@login_required(login_url='/login/')
def create_request(request):
    """
	Creación de la solicitud.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el actor
    actor = request.user.actor

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = CreateRequestForm(request.POST, user=request.user)
        if (form.is_valid()):
            # Crea la solicitud
            description = form.cleaned_data["description"]
            followed = form.cleaned_data["followed"]

            # Se comprueba que no sea el mismo usuario
            if followed == actor:
                raise PermissionDenied

            # Mensaje para el que envia
            pendingRequest = Request.objects.create(description=description, follower=actor, followed=followed,
                                                    copy=False)

            # Copia del mensaje para el receptor
            requestCopy = Request.objects.create(description=description, follower=actor, followed=followed, copy=True)

            pendingRequest.save()
            requestCopy.save()

            return HttpResponseRedirect('/requests/listSent')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = CreateRequestForm(user=request.user)

        # Datos del modelo (vista)

    # TODO las request denegadas si que se pueden volver a solicitar despues
    # Recupera todas las peticiones pendientes ha enviado el actor
    actorFollower = Request.objects.filter(follower=actor, copy=False, status='Pendiente')

    # Recupera todas las peticiones aceptadas ha enviado el actor
    actorFollower = actorFollower | Request.objects.filter(follower=actor, copy=False, status='Aceptada')

    # Recupera todas las peticiones pendientes que ha recibido el actor
    actorFollowed = Request.objects.filter(followed=actor, copy=False, status='Pendiente')

    # Recupera todas las peticiones aceptadas que ha recibido el actor
    actorFollowed = actorFollowed | Request.objects.filter(followed=actor, copy=False, status='Aceptada')

    actors = Actor.objects.all()

    # Excluye a los actores a los que ha enviado una petición
    for requestSent in actorFollower:
        if requestSent.follower == actor:
            actors = actors.exclude(pk=requestSent.followed.pk)

    # Excluye a los actores de los que ha recibido una petición
    for requestReceived in actorFollowed:
        if requestReceived.followed == actor:
            actors = actors.exclude(pk=requestReceived.follower.pk)

    # Excluye al actor que esta creando la solicitud
    actors = actors.exclude(pk=actor.pk)

    data = {
        'form': form,
        'title': 'Crea la solicitud',
        'year': datetime.now().year,
        'actors': actors,
    }

    return render(request, 'create_request.html', data)


# ACEPTAR PETICIONES
@login_required(login_url='/login/')
@csrf_exempt
def accept_request(request, pk):
    # Recupera la solicitud enviada
    pendingRequest = get_object_or_404(Request, pk=pk)

    # Recupera la request autentica
    pendingRequestCopy = Request.objects.get(follower=pendingRequest.follower, followed=pendingRequest.followed,
                                             copy=False, status='Pendiente')

    # Recupera el actor logueado
    actor = request.user.actor

    # Comprueba que sea su solicitud, que es copia y que está pendiente
    if pendingRequest.followed != actor or not pendingRequest.copy or pendingRequest.status != 'Pendiente':
        raise PermissionDenied

    # Setea el estado a Aceptada en la solicitud enviada
    pendingRequest.status = Request.StatusType[1][0]
    pendingRequest.save()

    # Setea el estado a Aceptada en la solicitud copia
    pendingRequestCopy.status = Request.StatusType[1][0]
    pendingRequestCopy.save()

    return HttpResponseRedirect('/requests/listReceived')


# RECHAZAR PETICIONES
@login_required(login_url='/login/')
@csrf_exempt
def reject_request(request, pk):
    # Recupera la solicitud enviada
    pendingRequest = get_object_or_404(Request, pk=pk)

    # Recupera la request autentica
    pendingRequestCopy = Request.objects.get(follower=pendingRequest.follower, followed=pendingRequest.followed,
                                             copy=False, status='Pendiente')

    # Recupera el actor logueado
    actor = request.user.actor

    # Comprueba que sea su solicitud, que sea copia y que esté en Pendiente
    if pendingRequest.followed != actor or not pendingRequest.copy or pendingRequest.status != 'Pendiente':
        raise PermissionDenied

    # Setea el estado a Rechazada en la solicitud enviada
    pendingRequest.status = Request.StatusType[2][0]
    pendingRequest.save()

    # Setea el estado a Recgazada en la solicitud copia
    pendingRequestCopy.status = Request.StatusType[2][0]
    pendingRequestCopy.save()

    return HttpResponseRedirect('/requests/listReceived')


# BORRAR PETICIONES ENVIADAS (solo no las mostramos)
@login_required(login_url='/login/')
def delete_request_sent(request, pk):
    requestSent = get_object_or_404(Request, pk=pk)

    actor = request.user.actor

    # Comprueba que sea su solicitud enviada y que no es copia
    if requestSent.follower != actor or requestSent.copy:
        raise PermissionDenied

    if request.method == 'POST':
        # Si aun está la solicitud pendiente y quiere cancelarla
        if requestSent.status == 'Pendiente':
            # Recupera la request copia para borrarla
            requestSentCopy = Request.objects.get(follower=requestSent.follower, followed=requestSent.followed,
                                                  copy=True, status='Pendiente')

            requestSent.delete()
            requestSentCopy.delete()

        else:
            # No borramos, seteamos el atributo boolean a True
            requestSent.deleted = True
            requestSent.save()

        return HttpResponseRedirect('/requests/listSent')

    data = {
        'actor': actor,
        'requestSent': requestSent,
    }

    return render(request, 'delete_request_sent.html', data)


# BORRAR PETICIONES RECIBIDAS
@login_required(login_url='/login/')
def delete_request_received(request, pk):
    requestReceived = get_object_or_404(Request, pk=pk)

    actor = request.user.actor

    # Comprueba que sea su solicitud enviada y es copia
    if requestReceived.followed != actor or not requestReceived.copy:
        raise PermissionDenied

    if request.method == 'POST':
        # Si esta pendiente la deniega
        if requestReceived.status == 'Pendiente':
            # Borramos la copia
            requestReceived.delete()
            # Recuperamos la autentica y la seteamos a Denegada
            requestReceivedCopy = Request.objects.get(follower=requestReceived.follower, followed=requestReceived.followed,
                                                      copy=False, status='Pendiente')
            requestReceivedCopy.status = Request.StatusType[2][0]
            requestReceivedCopy.save()
        else:
            # Borramos la copia
            requestReceived.delete()

        return HttpResponseRedirect('/requests/listReceived')

    data = {
        'actor': actor,
        'requestReceived': requestReceived,
    }

    return render(request, 'delete_request_received.html', data)


# ENVIAR PETICIÓN (listado usuarios NO amigos)
@login_required(login_url='/login/')
def send_request(request, pk):
    """
	Enviar solicitud.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el actor
    actor = request.user.actor

    # Recupera el actor al que va a enviar la petición
    followed = get_object_or_404(Actor, pk=pk)

    # Se comprueba que no sea el mismo usuario
    if followed == actor:
        raise PermissionDenied

    # COMPROBAR QUE YA ES AMIGO
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
        if friend == followed:
            isFriend = True

    # En el caso de que sea amigo no puede enviar
    if isFriend:
        messages.error(request, "Ya es su amigo, vuelva atrás y recargue la página")
        raise PermissionDenied

    # Recupera las peticiones que ha enviado a ese actor
    reqSentToActor = Request.objects.filter(follower=actor, followed=followed, copy=False)

    # En el caso de que exista una solicitud entre ambos actores, comprueba que no esté pendiente o aceptada
    for reqSent in reqSentToActor:
        if reqSent.status == 'Pendiente' or reqSent.status == 'Aceptada':
            messages.error(request, "Ya existe una solicitud pendiente, vuelva atrás y recargue la página")
            raise PermissionDenied

    # Recupera todas las peticiones que ha recibido el actor
    reqReceivedFromActor = Request.objects.filter(follower=followed, followed=actor, copy=False)

    # En el caso de que exista una solicitud entre ambos actores, comprueba que no esté pendiente o aceptada
    for reqReceived in reqReceivedFromActor:
        if reqReceived.status == 'Pendiente' or reqReceived.status == 'Aceptada':
            messages.error(request, "Ya existe una solicitud pendiente, vuelva atrás y recargue la página")
            raise PermissionDenied

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = SendRequestForm(request.POST)
        if (form.is_valid()):
            # Crea la solicitud
            description = form.cleaned_data["description"]


            # Solicitud para el que envia
            pendingRequest = Request.objects.create(description=description, follower=actor, followed=followed,
                                                    copy=False)

            # Copia del mensaje para el receptor
            requestCopy = Request.objects.create(description=description, follower=actor, followed=followed, copy=True)

            pendingRequest.save()
            requestCopy.save()

            return HttpResponseRedirect('/requests/listSent')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = SendRequestForm()

        # Datos del modelo (vista)

    data = {
        'form': form,
        'title': 'Envía la solicitud',
        'year': datetime.now().year,
        # Actor al que se envia la petición
        'followed': followed,
    }

    return render(request, 'send_request.html', data)