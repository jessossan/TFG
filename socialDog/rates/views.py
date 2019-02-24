from datetime import datetime
from dogs.models import Dog
from rates.forms import CreateRateForm, EditRateForm
from rates.models import Rate
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.



@login_required(login_url='/login/')
def create_rate(request, pk):
    """
	Crear valoración.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el actor
    actor = request.user.actor

    # Recupera el perro al que va a comentar
    dog = get_object_or_404(Dog, pk=pk)

    # Comprueba que no valore el criador a su perro
    if hasattr(request.user.actor, 'breeder') and dog.breeder == request.user.actor.breeder:
        return HttpResponseForbidden()

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = CreateRateForm(request.POST)
        if (form.is_valid()):
            # Crea la valoración
            stars = form.cleaned_data["stars"]
            if stars is None:
                stars = 0
            description = form.cleaned_data["description"]

            # Creación de la valoración
            rate = Rate.objects.create(stars=stars, description=description, creator_rate=actor, dog=dog)

            rate.save()

            return HttpResponseRedirect('/dogs/profile/' + str(dog.pk))

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = CreateRateForm()

        # Datos del modelo (vista)

    data = {
        'form': form,
        'title': 'Crea la valoración',
        'year': datetime.now().year,
        # Perro al que se envia la valoración
        'dog': dog,
    }

    return render(request, 'create_rate.html', data)


@login_required(login_url='/login/')
def delete_rate(request, pk):
    actor = request.user.actor

    # Recupera la valoración que esta editando
    rate = get_object_or_404(Rate, pk=pk)

    # Recupera el perro al que ha comentado
    dog = get_object_or_404(Dog, pk=rate.dog.pk)

    # Comprueba que sea su valoración
    if actor != rate.creator_rate:
        return HttpResponseForbidden()

    # Comprobar que no comente a su perro
    if request.method == 'POST':
        rate.delete()
        return HttpResponseRedirect('/dogs/profile/' + str(dog.pk))

    data = {
        'actor': actor,
        'dog': dog,
        'rate': rate,
    }

    return render(request, 'delete_rate.html', data)


@login_required(login_url='/login/')
def edit_rate(request, pk):
    """
	Edición de la valoración.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el actor logueado
    actor = request.user.actor

    # Recupera la valoración que esta editando
    rate = get_object_or_404(Rate, pk=pk)

    # Recupera el perro al que ha comentado
    dog = get_object_or_404(Dog, pk=rate.dog.pk)

    # Comprueba que sea su valoración
    if actor != rate.creator_rate:
        return HttpResponseForbidden()

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditRateForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Recupera la valoración
            stars = form.cleaned_data["stars"]
            description = form.cleaned_data["description"]

            rate.stars = stars
            rate.description = description

            rate.save()

            return HttpResponseRedirect('/dogs/profile/' + str(dog.pk))

    # Si se accede al form vía GET o cualquier otro método
    else:
        # Datos del modelo (vista)
        dataForm = {'stars': rate.stars, 'description': rate.description}
        form = EditRateForm(dataForm)

    data = {
        'form': form,
        'title': 'Edición de la valoración',
        'year': datetime.now().year,
        'rate': rate,
        'dog': dog,
    }

    return render(request, 'edit_rate.html', data)