from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from MYrequests.forms import CreateRequestForm
from MYrequests.models import Request
from actors.models import Actor


# LISTADO DE SOLICITUDES ENVIADAS

@login_required(login_url='/login/')
def list_requests_sent(request):
    # Recupera el actor logueado
    actor = request.user.actor

    try:
        # Ordenado por Aceptada, Denegada y Pendiente
        request_list_aux = Request.objects.all().filter(follower=actor).filter(copy=False).order_by('status')

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
        request_list_aux = Request.objects.all().filter(followed=actor).filter(copy=False).order_by('-status')

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

            # Se comprueba que no sea el mismo usuario, que no sea amigo ya
            if followed == actor:
                raise PermissionDenied

            # Mensaje para el que envia
            pendingRequest = Request.objects.create(description=description, follower=actor, followed=followed, copy=False)

            # Copia del mensaje para el receptor
            requestCopy = Request.objects.create(description=description, follower=actor, followed=followed, copy=True)

            pendingRequest.save()
            requestCopy.save()

            return HttpResponseRedirect('/requests/listSent')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = CreateRequestForm(user=request.user)

        # Datos del modelo (vista)

    # Recupera todas las peticiones que ha enviado el actor
    actorFollower = Request.objects.filter(follower=actor, copy=False)

    # Recupera todas las peticiones que ha recibido el actor
    actorFollowed = Request.objects.filter(followed=actor, copy=False)

    actors = Actor.objects.all()

    # Excluye a los actores a los que ha enviado una petición
    for requestSent in actorFollower:
        if requestSent.follower == actor:
            actors = actors.exclude(pk=requestSent.followed.pk)

    # Excluye a los actores de los que ha recibido una petición
    for requestSent in actorFollowed:
        if requestSent.followed == actor:
            actors = actors.exclude(pk=requestSent.follower.pk)

    # Excluye al actor que esta creando el mensaje
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

    # Recupera la request copia
    pendingRequestCopy = Request.objects.get(follower=pendingRequest.follower, followed=pendingRequest.followed,
                                             copy=True)

    # Recupera el actor logueado
    actor = request.user.actor

    # Comprueba que sea su solicitud y que es copia
    if pendingRequest.followed != actor or pendingRequest.copy or pendingRequest.status != 'Pending':
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

    # Recupera la request copia
    pendingRequestCopy = Request.objects.get(follower=pendingRequest.follower, followed=pendingRequest.followed,
                                             copy=True)

    # Recupera el actor logueado
    actor = request.user.actor

    # Comprueba que sea su solicitud, que sea copia y que esté en Pendiente
    if pendingRequest.followed != actor or pendingRequest.copy or pendingRequest.status != 'Pending':
        raise PermissionDenied

    # Setea el estado a Rechazada en la solicitud enviada
    pendingRequest.status = Request.StatusType[2][0]
    pendingRequest.save()

    # Setea el estado a Recgazada en la solicitud copia
    pendingRequestCopy.status = Request.StatusType[2][0]
    pendingRequestCopy.save()

    return HttpResponseRedirect('/requests/listReceived')
