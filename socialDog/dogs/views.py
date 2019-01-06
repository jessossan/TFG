from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from datetime import datetime
from actors.decorators import user_is_breeder
from actors.models import Breeder
from breeds.models import Breed
from dogs.forms import RegisterDogForm
from dogs.models import Dog


# Create your views here.

# LISTADO DE ANIMALES
def list_dogs(request):
    ownDog = False
    try:
        dog_list_aux = Dog.objects.all()

    except Exception as e:

        dog_list_aux = Dog.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(dog_list_aux, 6)

    try:
        dog_list_aux = paginator.page(page)
    except PageNotAnInteger:
        dog_list_aux = paginator.page(1)
    except EmptyPage:
        dog_list_aux = paginator.page(paginator.num_pages)

    data = {
        'dog_list': dog_list_aux,
        'title': 'Listado de perros',
        'ownDog': ownDog,
    }
    return render(request, 'list.html', data)

# LISTADO DE MIS ANIMALES
@login_required(login_url='/login/')
@user_is_breeder
def list_myDogs(request):

    # Recupera el criador
    breeder = request.user.actor.breeder
    ownDog = True

    try:
        dog_list_aux = Dog.objects.filter(breeder=breeder)

    except Exception as e:

        dog_list_aux = Dog.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(dog_list_aux, 6)

    try:
        dog_list_aux = paginator.page(page)
    except PageNotAnInteger:
        dog_list_aux = paginator.page(1)
    except EmptyPage:
        dog_list_aux = paginator.page(paginator.num_pages)

    data = {
        'dog_list': dog_list_aux,
        'title': 'Listado de mis perros',
        'ownDog': ownDog,
    }
    return render(request, 'list.html', data)

@login_required(login_url='/login/')
@user_is_breeder
def register_dog(request):
    """
	Registro del perro en el sistema.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el criador
    breeder = request.user.actor.breeder

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = RegisterDogForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Crea el perro
            name = form.cleaned_data["name"]
            age = form.cleaned_data["age"]
            gender = form.cleaned_data["gender"]
            descendant = form.cleaned_data["descendant"]
            details = form.cleaned_data["details"]
            photo = form.cleaned_data["photo"]
            awards = form.cleaned_data["awards"]
            breed = form.cleaned_data["breed"]

            dog = Dog.objects.create(name=name, age=age, gender=gender, descendant=descendant,
                                     details=details, photo=photo, awards=awards, breeder = breeder, breed = breed)

            dog.save()

            return HttpResponseRedirect('/dogs/list')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = RegisterDogForm()

        # Datos del modelo (vista)
        genders = form.fields["gender"].choices


    breeds = Breed.objects.all()
    data = {
        'form': form,
        'title': 'Registro de Perro',
        'year': datetime.now().year,
        'breeds': breeds,
        'genders': genders,
    }

    return render(request, 'register.html', data)
