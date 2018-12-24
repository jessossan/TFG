from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required


# Create your views here.
from stdnum.es import cif

from actors.decorators import user_is_customer, user_is_association, user_is_breeder
from actors.forms import EditBreederPass, EditBreederProfile, EditCustomerPass, EditCustomerProfile, \
    EditAssociationProfile, EditAssociationPass
from provinces.models import Province

"""USUARIO""" # USUARIO

@login_required(login_url='/login/')
@user_is_customer
def edit_profile_customer(request):
    """
    Edición del perfil Usuario
    """

    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    customer = request.user.actor.customer

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditCustomerProfile(request.POST, request.FILES)
        if (form.is_valid()):
            # Actualiza el User (model Django) en BD
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            userAccount = request.user
            userAccount.email = email
            userAccount.first_name = first_name
            userAccount.last_name = last_name
            userAccount.save()

            # Actualiza el Usuario en BD
            phone = form.cleaned_data["phone"]
            email = form.cleaned_data["email"]
            photo = form.cleaned_data["photo"]
            dni = form.cleaned_data["dni"]

            customer.phone = phone
            customer.photo = photo
            customer.dni = dni
            customer.email = email
            customer.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        dataForm = {'first_name': customer.userAccount.first_name, 'last_name': customer.userAccount.last_name,
                    'email': customer.userAccount.email,
                    'phone': customer.phone, 'dni': customer.dni, 'photo': customer.photo}
        form = EditCustomerProfile(dataForm)

    # Datos del modelo (vista)
    data = {
        'form': form,
        'customer': customer,
        'titulo': 'Editar Perfil'
    }

    return render(request, 'users/editUserProfile.html', data)

@login_required(login_url='/login/')
@user_is_customer
def edit_pass_customer(request):
    """Edición de la clave del usuario """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditCustomerPass(request.POST)
        if (form.is_valid()):
            # Se asegura que la Id que viene del formulario es la misma que la del usuario que realiza la acción
            userAccountId = form.cleaned_data["userAccountId"]
            userAccount = request.user
            if (userAccountId != userAccount.id):
                return HttpResponseForbidden()

            # Establece la nueva contraseña del usuario
            password = form.cleaned_data["password"]
            userAccount.set_password(password)
            userAccount.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = EditCustomerPass()

    # Datos del modelo (vista)
    data = {
        'form': form,
        'userAccount': request.user,
        'titulo': 'Cambiar credenciales',
    }

    return render(request, 'users/editUserPass.html', data)



"""CRIADOR""" # CRIADOR

@login_required(login_url='/login/')
@user_is_breeder
def edit_profile_breeder(request):
    """
    Edición del perfil Breeder
    """

    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    breeder = request.user.actor.breeder

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditBreederProfile(request.POST, request.FILES, user=request.user)
        if (form.is_valid()):
            # Actualiza el User (model Django) en BD
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            userAccount = request.user
            userAccount.email = email
            userAccount.first_name = first_name
            userAccount.last_name = last_name
            userAccount.save()

            # Actualiza el Criador en BD
            phone = form.cleaned_data["phone"]
            email = form.cleaned_data["email"]
            photo = form.cleaned_data["photo"]
            cif = form.cleaned_data["cif"]
            opening = form.cleaned_data["opening"]
            closing = form.cleaned_data["closing"]
            address = form.cleaned_data["address"]
            private = form.cleaned_data["private"]
            postalCode = form.cleaned_data["postalCode"]
            centerName = form.cleaned_data["centerName"]
            province = form.cleaned_data["province"]

            breeder.phone = phone
            breeder.photo = photo
            breeder.cif = cif
            breeder.email = email
            breeder.opening = opening
            breeder.closing = closing
            breeder.address = address
            breeder.private = private
            breeder.postalCode = postalCode
            breeder.centerName = centerName
            breeder.province = province
            breeder.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        # elimina las provincias duplicadas
        provincesAux = Province.objects.all().exclude(pk=breeder.province.pk)

        dataForm = {'first_name': breeder.userAccount.first_name, 'last_name': breeder.userAccount.last_name,
                    'email': breeder.userAccount.email,'opening': breeder.opening, 'closing': breeder.closing,
                    'phone': breeder.phone, 'cif': breeder.cif, 'photo': breeder.photo, 'address': breeder.address,
                    'private': breeder.private, 'postalCode': breeder.postalCode, 'centerName': breeder.centerName,
                    'province': breeder.province}
        form = EditBreederProfile(dataForm, user=request.user)

    # Datos del modelo (vista)
    data = {
        'form': form,
        'breeder': breeder,
        'provincesAux': Province.objects.all().exclude(pk=breeder.province.pk),
        'titulo': 'Editar Perfil'
    }

    return render(request, 'breeders/editBreederProfile.html', data)

@login_required(login_url='/login/')
@user_is_breeder
def edit_pass_breeder(request):
    """Edición de la clave del usuario """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditBreederPass(request.POST)
        if (form.is_valid()):
            # Se asegura que la Id que viene del formulario es la misma que la del usuario que realiza la acción
            userAccountId = form.cleaned_data["userAccountId"]
            userAccount = request.user
            if (userAccountId != userAccount.id):
                return HttpResponseForbidden()

            # Establece la nueva contraseña del usuario
            password = form.cleaned_data["password"]
            userAccount.set_password(password)
            userAccount.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = EditBreederPass()

    # Datos del modelo (vista)
    data = {
        'form': form,
        'userAccount': request.user,
        'titulo': 'Cambiar credenciales',
    }

    return render(request, 'breeders/editBreederPass.html', data)



"""ASSOCIATION""" # ASSOCIATION

@login_required(login_url='/login/')
@user_is_association
def edit_profile_association(request):
    """
    Edición del perfil ASSOCIATION
    """

    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    association = request.user.actor.association

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditAssociationProfile(request.POST, request.FILES, user=request.user)
        if (form.is_valid()):
            # Actualiza el User (model Django) en BD
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            userAccount = request.user
            userAccount.email = email
            userAccount.first_name = first_name
            userAccount.last_name = last_name
            userAccount.save()

            # Actualiza el association en BD
            phone = form.cleaned_data["phone"]
            email = form.cleaned_data["email"]
            photo = form.cleaned_data["photo"]
            cif = form.cleaned_data["cif"]
            opening = form.cleaned_data["opening"]
            closing = form.cleaned_data["closing"]
            address = form.cleaned_data["address"]
            private = form.cleaned_data["private"]
            postalCode = form.cleaned_data["postalCode"]
            centerName = form.cleaned_data["centerName"]
            province = form.cleaned_data["province"]

            association.phone = phone
            association.photo = photo
            association.cif = cif
            association.email = email
            association.opening = opening
            association.closing = closing
            association.address = address
            association.private = private
            association.postalCode = postalCode
            association.centerName = centerName
            association.province = province

            association.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        # elimina las provincias duplicadas
        provincesAux = Province.objects.all().exclude(pk=association.province.pk)

        dataForm = {'first_name': association.userAccount.first_name, 'last_name': association.userAccount.last_name,
                    'email': association.userAccount.email, 'centerName': association.centerName, 'province': association.province,
                    'phone': association.phone, 'cif': association.cif, 'photo': association.photo, 'opening': association.opening, 'closing': association.closing,
                    'address': association.address, 'private': association.private, 'postalCode': association.postalCode}
        form = EditAssociationProfile(dataForm, user=request.user)

    # Datos del modelo (vista)
    data = {
        'form': form,
        'association': association,
        # elimina las provincias duplicadas
        'provincesAux': Province.objects.all().exclude(pk=association.province.pk),
        'titulo': 'Editar Perfil'
    }

    return render(request, 'associations/editAssociationProfile.html', data)

@login_required(login_url='/login/')
@user_is_association
def edit_pass_association(request):
    """Edición de la clave del association """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditAssociationPass(request.POST)
        if (form.is_valid()):
            # Se asegura que la Id que viene del formulario es la misma que la del usuario que realiza la acción
            userAccountId = form.cleaned_data["userAccountId"]
            userAccount = request.user
            if (userAccountId != userAccount.id):
                return HttpResponseForbidden()

            # Establece la nueva contraseña del usuario
            password = form.cleaned_data["password"]
            userAccount.set_password(password)
            userAccount.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = EditAssociationPass()

    # Datos del modelo (vista)
    data = {
        'form': form,
        'userAccount': request.user,
        'titulo': 'Cambiar credenciales',
    }

    return render(request, 'associations/editAssociationPass.html', data)