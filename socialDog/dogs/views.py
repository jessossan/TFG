from builtins import Exception

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from actors.decorators import user_is_breeder
from actors.models import Breeder, Actor
from breeds.models import Breed
from comments.models import Comment
from dogs.forms import RegisterDogForm, EditDogForm
from dogs.models import Dog


# Create your views here.

# LISTADO DE ANIMALES
from likesDislikes.models import LikeDislike
from rates.models import Rate


def list_dogs(request):
    ownDog = False
    try:
        dog_list_aux = Dog.objects.all().order_by('name')

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
    return render(request, 'list_dog.html', data)


# CRIADOR: ANIMALES
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
    return render(request, 'list_dog.html', data)


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

            # Asigna imagen por defecto si no añade imagen
            if photo == None:
                photo = 'uploads/default-dog.png'

            dog = Dog.objects.create(name=name, age=age, gender=gender, descendant=descendant,
                                     details=details, photo=photo, awards=awards, breeder=breeder, breed=breed)

            dog.save()

            return HttpResponseRedirect('/dogs/ownList')

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

    return render(request, 'register_dog.html', data)


@login_required(login_url='/login/')
@user_is_breeder
def delete_dog(request, pk):
    breeder = request.user.actor.breeder
    dog = get_object_or_404(Dog, pk=pk)

    if breeder.pk != dog.breeder.pk:
        return HttpResponseForbidden()

    if request.method == 'POST':
        dog.delete()
        return HttpResponseRedirect('/dogs/ownList')

    data = {
        'breeder': breeder,
        'dog': dog,
    }

    return render(request, 'delete_dog.html', data)


@login_required(login_url='/login/')
@user_is_breeder
def edit_dog(request, pk):
    """
	Edición del perro.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el criador
    breeder = request.user.actor.breeder

    # Recupera el perro
    dog = get_object_or_404(Dog, pk=pk)

    # Comprueba que esta editando a su perro
    if breeder.pk != dog.breeder.pk:
        return HttpResponseForbidden()

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditDogForm(request.POST, request.FILES)
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

            dog.name = name
            dog.age = age
            dog.gender = gender
            dog.descendant = descendant
            dog.details = details
            # Evita que se actualice la foto
            if photo != None:
                dog.photo = photo
            dog.awards = awards
            dog.breed = breed

            dog.save()

            return HttpResponseRedirect('/dogs/ownList')

    # Si se accede al form vía GET o cualquier otro método
    else:
        # Datos del modelo (vista)
        dataForm = {'name': dog.name, 'age': dog.age, 'gender': dog.gender, 'descendant': dog.descendant,
                    'details': dog.details, 'photo': dog.photo, 'awards': dog.awards, 'breed': dog.breed}
        form = EditDogForm(dataForm)

    genders = form.fields["gender"].choices
    breeds = Breed.objects.all()
    data = {
        'form': form,
        'title': 'Edición de Perro',
        'year': datetime.now().year,
        'breeds': breeds,
        'genders': genders,
        'breed': dog.breed,
        'breedsAux': Breed.objects.all().exclude(pk=dog.breed.pk),  # Elimina la raza duplicada
    }

    return render(request, 'edit_dog.html', data)


# PERFIL: MOSTRAR ANIMALES
@login_required(login_url='/login/')
def list_profile_dogs(request, pk):
    # Recupera el criador
    breeder = get_object_or_404(Breeder, pk=pk)
    ownDog = False

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
        'title': 'Listado de perros del criador',
        'ownDog': ownDog,
    }
    return render(request, 'list_dog.html', data)


@login_required(login_url='/login/')
def dog_profile(request, pk):

    # Perro del que va a ver el perfil
    dog = get_object_or_404(Dog, pk=pk)

    # Recupera el actor logueado
    actor = request.user.actor

    # Comprueba que si es su propio perro no puede comentar
    ownDog = False
    if hasattr(request.user.actor, 'breeder') and dog.breeder == request.user.actor.breeder:
        ownDog = True


    ############# COMENTARIOS  ########################
    try:
        comment_list_aux = Comment.objects.all().filter(dog=dog).order_by('-creationDate')

    except Exception as e:

        comment_list_aux = Comment.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(comment_list_aux, 6)

    try:
        comment_list_aux = paginator.page(page)
    except PageNotAnInteger:
        comment_list_aux = paginator.page(1)
    except EmptyPage:
        comment_list_aux = paginator.page(paginator.num_pages)

    ######### VALORACIONES ########################
    rate_average = 0
    try:
        rate_list_aux = Rate.objects.all().filter(dog=dog).order_by('-creationDate')
        # Calculamos la media de valoraciones
        for rate in rate_list_aux:
            rate_average += rate.stars
        if rate_average != 0:
            rate_average = rate_average/rate_list_aux.count()

        # Redondeo
        rate_average = round(rate_average, 1)
        # Comprobación 0
        if rate_average <= 0.2:
            rate_average = 0
        # Comprobación 0.5
        elif rate_average > 0.2 and rate_average <= 0.6 :
            rate_average = 0.5
        # Comprobación 1
        elif rate_average > 0.6 and rate_average <= 1.2:
            rate_average = 1
        # Comprobación 1.5
        elif rate_average > 1.2 and rate_average <= 1.6:
            rate_average = 1.5
        # Comprobación 2
        elif rate_average > 1.6 and rate_average <= 2.2:
            rate_average = 2
        # Comprobación 2.5
        elif rate_average > 2.2 and rate_average <= 2.6:
            rate_average = 2.5
        # Comprobación 3
        elif rate_average > 2.6 and rate_average <= 3.2:
            rate_average = 3
        # Comprobación 3.5
        elif rate_average > 3.2 and rate_average <= 3.6:
            rate_average = 3.5
        # Comprobación 4
        elif rate_average > 3.6 and rate_average <= 4.2:
            rate_average = 4
        # Comprobación 4.5
        elif rate_average > 4.2 and rate_average <= 4.6:
            rate_average = 4.5
        # Comprobación 5
        elif rate_average >= 4.6:
            rate_average = 5

    except Exception as e:

        rate_list_aux = Rate.objects.none()

    ########## LIKES / DISLIKES ####################
    commentWithLikes = Comment.objects.none()
    commentWithDislikes = Comment.objects.none()
    try:
        # Recupera los likes del actor
        likes = LikeDislike.objects.all().filter(actor=actor, like=True)

        # Recupera los dislikes del actor
        dislikes = LikeDislike.objects.all().filter(actor=actor, like=False)



        # Recupera los comentarios con like del actor al perro del perfil
        for commentLiked in likes:
            commentWithLikes = commentWithLikes | Comment.objects.all().filter(pk=commentLiked.comment.pk, dog=dog)

        # Recupera los comentarios con dislike del actor al perro del perfil
        for commentDisliked in dislikes:
            commentWithDislikes = commentWithDislikes | Comment.objects.all().filter(pk=commentDisliked.comment.pk, dog=dog)

    except Exception as e:

        rate_list_aux = Rate.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(rate_list_aux, 6)

    try:
        rate_list_aux = paginator.page(page)
    except PageNotAnInteger:
        rate_list_aux = paginator.page(1)
    except EmptyPage:
        rate_list_aux = paginator.page(paginator.num_pages)

    rate_size = Rate.objects.all().filter(dog=dog).count()
    data = {
        'dog': dog,
        'actor': actor,
        'comment_list': comment_list_aux,
        'ownDog': ownDog,
        'title': 'Perfil del perro',
        'commentWithLikes': commentWithLikes,
        'commentWithDislikes': commentWithDislikes,
        'average': rate_average,
        'rateSize': rate_size,
    }
    return render(request, 'dog_profile.html', data)
