from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, date
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.template import loader

# Create your views here.
from actors.models import Customer, Association, Breeder, Actor
from breeds.models import Breed
from events.models import Event
from news.models import News
from provinces.models import Province
from web.forms import RegisterCustomerForm, RegisterAssociationForm, RegisterBreederForm


def index(request):
    template = loader.get_template('welcome/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


# EXCEPCIONES

def error400(request, *args, **kwargs):
    data = {
        'user': request.user,
    }
    return render(request, '400.html', data)


def error403(request, *args, **kwargs):
    data = {
        'user': request.user,
    }
    return render(request, '403.html', data)


def error404(request, *args, **kwargs):
    data = {
        'user': request.user,
    }
    return render(request, '404.html', data)


def error500(request, *args, **kwargs):
    data = {
        'user': request.user,
    }
    return render(request, '500.html', data)


# REGISTROS

def register_customer(request):
    """
	Registro del Usuario en el sistema.
	"""
    assert isinstance(request, HttpRequest)

    # Valida que el usuario sea anónimo (no registrado)
    if (request.user.is_authenticated):
        return HttpResponseRedirect('/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = RegisterCustomerForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Guarda el User (model Django) en BD
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Crea el Usuario y lo asocia al User anterior
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            dni = form.cleaned_data["dni"]
            userAccount = user

            # Asigna imagen por defecto si no añade imagen
            if photo == None:
                photo = 'uploads/default.jpg'

            customer = Customer.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount, people=0)

            user = User.objects.get(username=username)

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)
            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = RegisterCustomerForm()

    # Datos del modelo (vista)

    data = {
        'form': form,
        'title': 'Registro de Usuario',
        'year': datetime.now().year,
    }

    return render(request, 'web/registerUser.html', data)


def register_association(request):
    """
	Registro de la Asociación en el sistema.
	"""
    assert isinstance(request, HttpRequest)

    # Valida que el usuario sea anónimo (no registrado)
    if (request.user.is_authenticated):
        return HttpResponseRedirect('/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = RegisterAssociationForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Guarda el User (model Django) en BD
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Crea la Asociación y lo asocia al User anterior
            centerName = form.cleaned_data["centerName"]
            postalCode = form.cleaned_data["postalCode"]
            province = form.cleaned_data["province"]
            address = form.cleaned_data["address"]
            opening = form.cleaned_data["opening"]
            closing = form.cleaned_data["closing"]
            cif = form.cleaned_data["cif"]
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            private = form.cleaned_data["private"]
            notes = form.cleaned_data["notes"]
            userAccount = user

            # Asigna imagen por defecto si no añade imagen
            if photo == None:
                photo = 'uploads/default.jpg'

            association = Association.objects.create(phone=phone, photo=photo, centerName=centerName,
                                                     postalCode=postalCode, province=province, address=address,
                                                     opening=opening, closing=closing, cif=cif, userAccount=userAccount,
                                                     people=0, private=private, notes=notes)

            user = User.objects.get(username=username)

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)
            return HttpResponseRedirect('/')
        else:
            provinces = Province.objects.all()

            # Busca la provincia específica cuando falla el form
            try:
                provinceSelected = form.cleaned_data["province"]

                # elimina las provincias duplicadas
                provincesAux = Province.objects.all().exclude(pk=provinceSelected.pk)
            except:
                provinceSelected = None
                provincesAux = None
    # Si se accede al form vía GET o cualquier otro método
    else:
        form = RegisterAssociationForm()

        # Datos del modelo (vista)
        provinces = Province.objects.all()
        provinceSelected = None
        provincesAux = None
    data = {
        'form': form,
        'title': 'Registro de Asociación',
        'year': datetime.now().year,
        'provinces': provinces,
        'provinceSelected': provinceSelected,
        'provincesAux': provincesAux,
    }

    return render(request, 'web/registerAssociation.html', data)


def register_breeder(request):
    """
	Registro de la Criador en el sistema.
	"""
    assert isinstance(request, HttpRequest)

    # Valida que el usuario sea anónimo (no registrado)
    if (request.user.is_authenticated):
        return HttpResponseRedirect('/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = RegisterBreederForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Guarda el User (model Django) en BD
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Crea la Criador y lo asocia al User anterior
            centerName = form.cleaned_data["centerName"]
            postalCode = form.cleaned_data["postalCode"]
            province = form.cleaned_data["province"]
            address = form.cleaned_data["address"]
            opening = form.cleaned_data["opening"]
            closing = form.cleaned_data["closing"]
            cif = form.cleaned_data["cif"]
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            private = form.cleaned_data["private"]
            breeds = form.cleaned_data["breeds"]
            notes = form.cleaned_data["notes"]
            userAccount = user

            # Asigna imagen por defecto si no añade imagen
            if photo == None:
                photo = 'uploads/default.jpg'

            breeder = Breeder.objects.create(phone=phone, photo=photo, centerName=centerName,
                                             postalCode=postalCode, province=province, address=address,
                                             opening=opening, closing=closing, cif=cif, userAccount=userAccount,
                                             people=0, private=private, notes=notes)
            # Añadir las razas al criador
            for breed in breeds:
                breeder.breeds.add(breed)

            user = User.objects.get(username=username)

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)
            return HttpResponseRedirect('/')

        else:
            provinces = Province.objects.all()

            # Busca la provincia específica seleccionada antes de que fallara el form
            try:
                provinceSelected = form.cleaned_data["province"]
                # elimina las provincias duplicadas
                provincesAux = Province.objects.all().exclude(pk=provinceSelected.pk)
            except:
                provinceSelected = None
                provincesAux = None

            # Busca la provincia específica seleccionada antes de que fallara el form
            try:
                breedsSelected = form.cleaned_data["breeds"]
                # recorre las razas seleccionadas antes de que fallara el form
                for b in breedsSelected:
                    # Quita las razas repetidas
                    breedsAux = Breed.objects.all().exclude(name=b.name)

            except:
                breedsSelected = None

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = RegisterBreederForm()

        # Datos del modelo (vista)
        provinces = Province.objects.all()
        provinceSelected = None
        breedsSelected = None
        breedsAux = None
        provincesAux = None

    breeds = Breed.objects.all()
    data = {
        'form': form,
        'title': 'Registro de Criador',
        'year': datetime.now().year,
        'provinces': provinces,
        'provinceSelected': provinceSelected,
        'breeds': breeds,
        'breedsSelected': breedsSelected,
        'breedsAux': breedsAux,
        'provincesAux': provincesAux
    }

    return render(request, 'web/registerBreeder.html', data)


# LISTADOS DE EVENTOS

@login_required(login_url='/login/')
def list_events(request):
    # Orden inverso para que los eventos nuevos creados salgan arriba de la lista
    events_list = Event.objects.all().order_by('-creationDate')

    data = {
        'event_list': events_list,
        'title': 'Listado de eventos',
        # Comprobación para controlar el color de boton de la vista
        'isEvent': True,

    }
    return render(request, 'welcome/events.html', data)


# LISTADOS DE NOTICIAS

@login_required(login_url='/login/')
def list_news(request):
    # Orden inverso para que las noticias nuevas creados salgan arriba de la lista
    news_list = News.objects.all().order_by('-creationDate')

    data = {
        'news_list': news_list,
        'title': 'Listado de noticias',
        # Comprobación para controlar el color de boton de la vista
        'isEvent': False,

    }
    return render(request, 'welcome/news.html', data)


## PERFIL USUARIO NO AUTENTICADO


def profile(request, pk):
    actor = get_object_or_404(Actor, pk=pk)

    try:
        if actor.breeder:
            actor = get_object_or_404(Breeder, pk=pk)
            if actor.private:
                return HttpResponseRedirect('/login/')
    except:
        try:
            if actor.association:
                actor = get_object_or_404(Association, pk=pk)
                if actor.private:
                    return HttpResponseRedirect('/login/')
        except:
            return HttpResponseForbidden()

    data = {
        'actor': actor,
        'title': 'Perfil del actor',
    }
    return render(request, 'web/profile.html', data)
