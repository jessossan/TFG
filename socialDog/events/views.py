from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from actors.decorators import user_is_breeder
from events.forms import CreateBreederEventForm, EditEventForm
from events.models import Event
from datetime import datetime


# Create your views here.


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

            # Asigna imagen por defecto si no añade imagen

            event = Event.objects.create(title=title, description=description, place=place, startDate=startDate,
                                         startTime=startTime, finishDate=finishDate, finishTime=finishTime,
                                         length=length, breeder=breeder)

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

    return render(request, 'create_event.html', data)


@login_required(login_url='/login/')
def list_myEvents(request):
    if hasattr(request.user.actor, 'breeder'):
        # Recupera el criador
        breeder = request.user.actor.breeder
        event_list_aux = Event.objects.filter(breeder=breeder)
        ownEvent = True

    elif hasattr(request.user.actor, 'association'):
        # Recupera la asociación
        association = request.user.actor.association
        event_list_aux = Event.objects.filter(association=association)
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

    data = {
        'event_list': event_list_aux,
        'title': 'Listado de mis eventos',
        'ownEvent': ownEvent,
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

            event.title = title
            event.place = place
            event.description = description
            event.startDate = startDate
            event.startTime = startTime
            event.finishDate = finishDate
            event.finishTime = finishTime
            event.length = length

            event.save()

            return HttpResponseRedirect('/events/ownList')

    # Si se accede al form vía GET o cualquier otro método
    else:
        # Datos del modelo (vista)
        dataForm = {'title': event.title,'place': event.place, 'description': event.description, 'startDate': event.startDate, 'startTime': event.startTime,
                    'finishDate': event.finishDate, 'finishTime': event.finishTime, 'length': event.length, }
        form = EditEventForm(dataForm)

    data = {
        'form': form,
        'title': 'Edición de evento',
        'year': datetime.now().year,
        'startDate': event.startDate,
        'startTime': event.startTime,
        'finishDate': event.finishDate,
        'finishTime': event.finishTime,
        'length': event.length,
    }

    return render(request, 'edit_event.html', data)
