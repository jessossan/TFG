from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from actors.decorators import user_is_breeder
from events.forms import CreateBreederEventForm
from events.models import Event
from datetime import datetime


# Create your views here.


@login_required(login_url='/login/')
@user_is_breeder
def create_breeder_event(request):
    """
	Registro del perro en el sistema.
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
            datetime.timetz()

            # Asigna imagen por defecto si no añade imagen

            event = Event.objects.create(title=title, description=description, place=place, startDate=startDate,
                                         startTime=startTime,finishDate=finishDate, finishTime= finishTime, length=length, breeder=breeder)

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

    elif hasattr(request.user.actor, 'association'):
        # Recupera la asociación
        association = request.user.actor.association
        event_list_aux = Event.objects.filter(association=association)

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
    }
    return render(request, 'list_event.html', data)
