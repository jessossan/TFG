from django.contrib.auth import login
from django.contrib.auth.models import User
from datetime import datetime, date
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

# Create your views here.
from actors.models import Customer, Association, Breeder
from provinces.models import Province
from web.forms import RegisterCustomerForm, RegisterAssociationForm


def index(request):
    template = loader.get_template('welcome/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


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
            userAccount = user

            association = Association.objects.create(phone=phone, photo=photo, centerName=centerName,
                                                  postalCode=postalCode, province=province, address=address,
                                                  opening=opening, closing=closing, cif=cif, userAccount=userAccount,
                                                  people=0, private = private)

            user = User.objects.get(username=username)

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)
            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = RegisterAssociationForm()

    # Datos del modelo (vista)
    provinces = Province.objects.all()
    provinceSelected = None
    data = {
        'form': form,
        'title': 'Registro de Asociación',
        'year': datetime.now().year,
        'provinces': provinces,
        'provinceSelected': provinceSelected,
    }

    return render(request, 'web/registerAssociation.html', data)
