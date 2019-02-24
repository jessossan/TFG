from datetime import datetime
from dogs.models import Dog
from rates.forms import CreateRateForm
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

            # Creación del comentario
            comment = Rate.objects.create(stars=stars, description=description, creator_rate=actor, dog=dog)

            comment.save()

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
