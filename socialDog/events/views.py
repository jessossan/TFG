from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from actors.decorators import user_is_breeder, user_is_association
from events.forms import CreateBreederEventForm, EditEventForm, CreateAssociationEventForm
from events.models import Event
from datetime import datetime, date


# Create your views here.

# CREACION EVENTO CRIADOR
@login_required(login_url='/login/')
@user_is_breeder
def create_breeder_event(request):
    """
	Registro del evento en el sistema.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el criador
    breeder = request.user.actor.breeder

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = CreateBreederEventForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Crea el evento
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            place = form.cleaned_data["place"]
            startDate = form.cleaned_data["startDate"]
            startTime = form.cleaned_data["startTime"]
            finishDate = form.cleaned_data["finishDate"]
            finishTime = form.cleaned_data["finishTime"]
            length = form.cleaned_data["length"]
            photo = form.cleaned_data["photo"]

            # Asigna imagen por defecto si no añade imagen
            if photo == None:
                photo = 'event-default.png'

            event = Event.objects.create(title=title, description=description, place=place, startDate=startDate,
                                         startTime=startTime, finishDate=finishDate, finishTime=finishTime,
                                         length=length,photo=photo, breeder=breeder)

            event.save()

            return HttpResponseRedirect('/events/ownList')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = CreateBreederEventForm()

        # Datos del modelo (vista)

    data = {
        'form': form,
        'title': 'Creación de evento',
        'year': datetime.now().year,
    }

    return render(request, 'create_breeder_event.html', data)


# CREACION EVENTO ASOCIACION
@login_required(login_url='/login/')
@user_is_association
def create_association_event(request):
    """
	Registro del evento en el sistema.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera la associacion
    association = request.user.actor.association

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = CreateAssociationEventForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Crea el evento
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            place = form.cleaned_data["place"]
            startDate = form.cleaned_data["startDate"]
            startTime = form.cleaned_data["startTime"]
            finishDate = form.cleaned_data["finishDate"]
            finishTime = form.cleaned_data["finishTime"]
            length = form.cleaned_data["length"]
            photo = form.cleaned_data["photo"]

            # Asigna imagen por defecto si no añade imagen
            if photo == None:
                photo = 'event-default.png'

            event = Event.objects.create(title=title, description=description, place=place, startDate=startDate,
                                         startTime=startTime, finishDate=finishDate, finishTime=finishTime,
                                         length=length, photo=photo, association=association)

            event.save()

            return HttpResponseRedirect('/events/ownList')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = CreateAssociationEventForm()

        # Datos del modelo (vista)

    data = {
        'form': form,
        'title': 'Creación de evento',
        'year': datetime.now().year,
    }

    return render(request, 'create_association_event.html', data)


# LISTADO DE TODOS MIS EVENTOS CRIADOR/ASOCIACIÓN
@login_required(login_url='/login/')
def list_myEvents(request):
    if hasattr(request.user.actor, 'breeder'):
        # Recupera el criador
        breeder = request.user.actor.breeder
        event_list_aux = Event.objects.filter(breeder=breeder).order_by('title')
        ownEvent = True

    elif hasattr(request.user.actor, 'association'):
        # Recupera la asociación
        association = request.user.actor.association
        event_list_aux = Event.objects.filter(association=association).order_by('title')
        ownEvent = True

    else:
        return HttpResponseForbidden()

    page = request.GET.get('page', 1)
    paginator = Paginator(event_list_aux, 6)

    try:
        event_list_aux = paginator.page(page)
    except PageNotAnInteger:
        event_list_aux = paginator.page(1)
    except EmptyPage:
        event_list_aux = paginator.page(paginator.num_pages)

    try:
        # Intenta sumar un dia
        tomorrow = date(date.today().year, date.today().month, date.today().day + 1)

    except Exception as e:
        # En caso de que sea ultimo dia del mes, suma 1 al mes y convierte el dia en 1
        error = e.args[0]
        dayOutOfRange = ''.join(['day is out of range for month',])
        monthOutOfRange = ''.join(['month must be in 1..12',])

        if error == dayOutOfRange:
            tomorrow = date(date.today().year, date.today().month+1, 1)

        # En caso de que sea ultimo mes del año, establece mes 1 dia 1 y suma 1 año
        elif error == monthOutOfRange:
            tomorrow = date(date.today().year +1, 1, 1)

    data = {
        'event_list': event_list_aux,
        'title': 'Listado de mis eventos',
        'ownEvent': ownEvent,
        # la fecha de hoy para que no salga el botón editar eventos pasados
        'today': date.today(),
        # la fecha de mañana para que no salga el boton de editar eventos con un día de antelación
        'tomorrow': tomorrow,
        'myEvents': True,
    }
    return render(request, 'list_event.html', data)


# LISTADO DE MIS EVENTOS POR REALIZAR CRIADOR/ASOCIACION
@login_required(login_url='/login/')
def list_myFutureEvents(request):
    if hasattr(request.user.actor, 'breeder'):
        # Recupera el criador
        breeder = request.user.actor.breeder
        # Filtro para recuperar los eventos del criador        Filtro para recuperar los eventos de hoy y futuros
        event_list_aux = Event.objects.filter(breeder=breeder).filter(startDate__gte=date.today()).order_by('title')
        ownEvent = True

    elif hasattr(request.user.actor, 'association'):
        # Recupera la asociación
        association = request.user.actor.association
        event_list_aux = Event.objects.filter(association=association).filter(startDate__gte=date.today()).order_by('title')
        ownEvent = True

    else:
        return HttpResponseForbidden()

    page = request.GET.get('page', 1)
    paginator = Paginator(event_list_aux, 6)

    try:
        event_list_aux = paginator.page(page)
    except PageNotAnInteger:
        event_list_aux = paginator.page(1)
    except EmptyPage:
        event_list_aux = paginator.page(paginator.num_pages)

    try:
        # Intenta sumar un dia
        tomorrow = date(date.today().year, date.today().month, date.today().day + 1)

    except Exception as e:
        # En caso de que sea ultimo dia del mes, suma 1 al mes y convierte el dia en 1
        error = e.args[0]
        dayOutOfRange = ''.join(['day is out of range for month',])
        monthOutOfRange = ''.join(['month must be in 1..12',])

        if error == dayOutOfRange:
            tomorrow = date(date.today().year, date.today().month+1, 1)

        # En caso de que sea ultimo mes del año, establece mes 1 dia 1 y suma 1 año
        elif error == monthOutOfRange:
            tomorrow = date(date.today().year +1, 1, 1)

    data = {
        'event_list': event_list_aux,
        'title': 'Listado de mis eventos',
        'ownEvent': ownEvent,
        # la fecha de hoy para que no salga el botón editar eventos pasados
        'today': date.today(),
        # la fecha de mañana para que no salga el boton de editar eventos con un día de antelación
        'tomorrow': tomorrow,
        'myFutureEvents': True,
    }
    return render(request, 'list_event.html', data)


# LISTADO DE MIS EVENTOS FINALIZADOS CRIADOR/ASOCIACION
@login_required(login_url='/login/')
def list_myPastEvents(request):
    if hasattr(request.user.actor, 'breeder'):
        # Recupera el criador
        breeder = request.user.actor.breeder
        # Filtro para recuperar los eventos del criador        Filtro para recuperar los eventos de hoy y futuros
        event_list_aux = Event.objects.filter(breeder=breeder).filter(startDate__lt=date.today()).order_by('title')
        ownEvent = True

    elif hasattr(request.user.actor, 'association'):
        # Recupera la asociación
        association = request.user.actor.association
        event_list_aux = Event.objects.filter(association=association).filter(startDate__lt=date.today()).order_by('title')
        ownEvent = True

    else:
        return HttpResponseForbidden()

    page = request.GET.get('page', 1)
    paginator = Paginator(event_list_aux, 6)

    try:
        event_list_aux = paginator.page(page)
    except PageNotAnInteger:
        event_list_aux = paginator.page(1)
    except EmptyPage:
        event_list_aux = paginator.page(paginator.num_pages)

    try:
        # Intenta sumar un dia
        tomorrow = date(date.today().year, date.today().month, date.today().day + 1)

    except Exception as e:
        # En caso de que sea ultimo dia del mes, suma 1 al mes y convierte el dia en 1
        error = e.args[0]
        dayOutOfRange = ''.join(['day is out of range for month',])
        monthOutOfRange = ''.join(['month must be in 1..12',])

        if error == dayOutOfRange:
            tomorrow = date(date.today().year, date.today().month+1, 1)

        # En caso de que sea ultimo mes del año, establece mes 1 dia 1 y suma 1 año
        elif error == monthOutOfRange:
            tomorrow = date(date.today().year +1, 1, 1)

    data = {
        'event_list': event_list_aux,
        'title': 'Listado de mis eventos',
        'ownEvent': ownEvent,
        # la fecha de hoy para que no salga el botón editar eventos pasados
        'today': date.today(),
        # la fecha de mañana para que no salga el boton de editar eventos con un día de antelación
        'tomorrow': tomorrow,
    }
    return render(request, 'list_event.html', data)


@login_required(login_url='/login/')
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    association = None
    breeder = None

    if hasattr(request.user.actor, 'breeder'):
        # Recupera el criador
        breeder = request.user.actor.breeder

        # Comprueba que sea su evento
        if event.breeder != breeder:
            return HttpResponseForbidden()

    elif hasattr(request.user.actor, 'association'):
        # Recupera la asociación
        association = request.user.actor.association

        # Comprueba que sea su evento
        if event.association != association:
            return HttpResponseForbidden()

    # Si no es criador o asociacion rechaza
    else:
        return HttpResponseForbidden()

    if request.method == 'POST':
        event.delete()
        return HttpResponseRedirect('/events/ownList')

    # Si el que esta borrando es asociación
    if association is not None:
        data = {
            'association': association,
            'event': event,
        }
    else:
        # Si el que esta borrando es criador
        data = {
            'breeder': breeder,
            'event': event,
        }

    return render(request, 'delete_event.html', data)


@login_required(login_url='/login/')
def edit_event(request, pk):
    """
	Edición del evento (para asociacion y criador).
	"""
    assert isinstance(request, HttpRequest)

    event = get_object_or_404(Event, pk=pk)
    association = None
    breeder = None

    if hasattr(request.user.actor, 'breeder'):
        # Recupera el criador
        breeder = request.user.actor.breeder

        # Comprueba que sea su evento
        if event.breeder != breeder:
            return HttpResponseForbidden()

    elif hasattr(request.user.actor, 'association'):
        # Recupera la asociación
        association = request.user.actor.association

        # Comprueba que sea su evento
        if event.association != association:
            return HttpResponseForbidden()

    # Si no es criador o asociacion rechaza
    else:
        return HttpResponseForbidden()

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditEventForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Recupera el evento
            title = form.cleaned_data["title"]
            place = form.cleaned_data["place"]
            description = form.cleaned_data["description"]
            startDate = form.cleaned_data["startDate"]
            startTime = form.cleaned_data["startTime"]
            finishDate = form.cleaned_data["finishDate"]
            finishTime = form.cleaned_data["finishTime"]
            length = form.cleaned_data["length"]
            photo = form.cleaned_data["photo"]

            event.title = title
            event.place = place
            event.description = description
            event.startDate = startDate
            event.startTime = startTime
            event.finishDate = finishDate
            event.finishTime = finishTime
            event.length = length
            if photo != None:
                event.photo = photo

            event.save()

            return HttpResponseRedirect('/events/ownList')

    # Si se accede al form vía GET o cualquier otro método
    else:
        # Datos del modelo (vista)
        dataForm = {'title': event.title, 'place': event.place, 'description': event.description,
                    'startDate': event.startDate, 'startTime': event.startTime,
                    'finishDate': event.finishDate, 'finishTime': event.finishTime, 'length': event.length, 'photo': event.photo}
        form = EditEventForm(dataForm)

    # Comprobación de que se pueda editar
    try:
        # Intenta sumar un dia
        tomorrow = date(date.today().year, date.today().month, date.today().day + 1)

    except Exception as e:
        # En caso de que sea ultimo dia del mes, suma 1 al mes y convierte el dia en 1
        error = e.args[0]
        dayOutOfRange = ''.join(['day is out of range for month', ])
        monthOutOfRange = ''.join(['month must be in 1..12', ])

        if error == dayOutOfRange:
            tomorrow = date(date.today().year, date.today().month + 1, 1)

        # En caso de que sea ultimo mes del año, establece mes 1 dia 1 y suma 1 año
        elif error == monthOutOfRange:
            tomorrow = date(date.today().year + 1, 1, 1)

    canEdit = True

    # si la fecha de comienzo del evento es pasada o menos de un día no se puede editar
    if (event.startDate <= date.today() or tomorrow == event.startDate):
        canEdit = False
    data = {
        'form': form,
        'title': 'Edición de evento',
        'year': datetime.now().year,
        'startDate': event.startDate,
        'startTime': event.startTime,
        'finishDate': event.finishDate,
        'finishTime': event.finishTime,
        'length': event.length,
        'canEdit': canEdit,
        'event': event,
    }

    return render(request, 'edit_event.html', data)
