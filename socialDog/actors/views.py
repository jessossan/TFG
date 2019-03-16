from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

from MYrequests.models import Request
from actors.decorators import user_is_customer, user_is_association, user_is_breeder
from actors.forms import EditBreederPass, EditBreederProfile, EditCustomerPass, EditCustomerProfile, \
    EditAssociationProfile, EditAssociationPass
from actors.models import Customer, Breeder, Association, Actor
from breeds.models import Breed
from provinces.models import Province
import django.contrib.auth.views
from django.contrib import messages

# Create your views here.


"""USUARIO"""  # USUARIO


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
            # Para que no se actualice la foto cuando se edite el perfil
            if (photo != None):
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


# ELIMINAR LA CUENTA DE UN USUARIO
@login_required(login_url='/login/')
@user_is_customer
def delete_customer_account(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.user.actor.customer.pk != customer.pk:
        return HttpResponseForbidden()

    if request.method == 'POST':
        User.objects.filter(pk=request.user.pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Se ha borrado su cuenta correctamente')
        return HttpResponseRedirect('/logout')

    return render(request, 'users/delete_user.html', {'customer': customer})


"""CRIADOR"""  # CRIADOR


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
            notes = form.cleaned_data["notes"]
            province = form.cleaned_data["province"]
            breeds = form.cleaned_data["breeds"]

            breeder.phone = phone

            # Para que no se actualice la foto cuando se edite el perfil
            if (photo != None):
                breeder.photo = photo

            breeder.cif = cif
            breeder.email = email
            breeder.opening = opening
            breeder.closing = closing
            breeder.address = address
            breeder.private = private
            breeder.postalCode = postalCode
            breeder.centerName = centerName
            breeder.notes = notes
            breeder.province = province

            # Elimina todas las razas que tenia
            breeder.breeds.set(Breed.objects.none())
            # Añade las nuevas razas
            breeder.breeds.set(breeds)

            breeder.save()

            return HttpResponseRedirect('/')
        # En el caso de que falle el form
        else:
            # Recupera las fechas de cierre y apertura cuando falla el form
            opening = form.cleaned_data["opening"]
            closing = form.cleaned_data["closing"]

            # Recupera la provincia del formulario en el caso que falle
            provinceSelected = form.cleaned_data["province"]
            # elimina las provincias duplicadas
            provincesAux = Province.objects.all().exclude(pk=provinceSelected.pk)

            # Recupera las razas
            breedsSelected = form.cleaned_data["breeds"]
            # recorre las razas seleccionadas antes de que fallara el form
            for b in breedsSelected:
                # Quita las razas repetidas
                breedsAux = Breed.objects.all().exclude(name=b.name)

    # Si se accede al form vía GET o cualquier otro método
    else:
        breedsSelected = breeder.breeds.all()
        # recorre las razas seleccionadas del criador
        for b in breedsSelected:
            # Quita las razas repetidas
            breedsAux = Breed.objects.all().exclude(name=b.name)

        # Recupera las fechas de apertura y cierre del criador (primera vez que se entra a la vista)
        opening = breeder.opening
        closing = breeder.closing

        # Recupera la provincia del criador
        provinceSelected = breeder.province

        dataForm = {'first_name': breeder.userAccount.first_name, 'last_name': breeder.userAccount.last_name,
                    'email': breeder.userAccount.email, 'opening': breeder.opening, 'closing': breeder.closing,
                    'phone': breeder.phone, 'cif': breeder.cif, 'photo': breeder.photo, 'address': breeder.address,
                    'notes': breeder.notes,
                    'private': breeder.private, 'postalCode': breeder.postalCode, 'centerName': breeder.centerName,
                    'province': breeder.province}
        form = EditBreederProfile(dataForm, user=request.user)

    # Recupera las provincias del criador sin duplicado
    provincesAux = Province.objects.all().exclude(pk=breeder.province.pk)

    # Datos del modelo (vista)
    data = {
        'form': form,
        'breeder': breeder,
        'breedsAux': breedsAux,
        'breedsSelected': breedsSelected,
        'opening': opening,  # Se recupera la hora de apertura para que se muestre correctamente en el form
        'closing': closing,  # Se recupera la hora de cierre para que se muestre correctamente en el form
        'provincesAux': provincesAux,
        'provinceSelected': provinceSelected,
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


# ELIMINAR LA CUENTA DE UN CRIADOR
@login_required(login_url='/login/')
@user_is_breeder
def delete_breeder_account(request, pk):
    breeder = get_object_or_404(Breeder, pk=pk)
    if request.user.actor.breeder.pk != breeder.pk:
        return HttpResponseForbidden()

    if request.method == 'POST':
        User.objects.filter(pk=request.user.pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Se ha borrado su cuenta correctamente')
        return HttpResponseRedirect('/logout')

    return render(request, 'breeders/delete_breeder.html', {'breeder': breeder})


"""ASSOCIATION"""  # ASSOCIATION


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
            notes = form.cleaned_data["notes"]
            province = form.cleaned_data["province"]

            association.phone = phone

            # Para que no se actualice la foto cuando se edite el perfil
            if (photo != None):
                association.photo = photo

            association.cif = cif
            association.email = email
            association.opening = opening
            association.closing = closing
            association.address = address
            association.private = private
            association.postalCode = postalCode
            association.centerName = centerName
            association.notes = notes
            association.province = province

            association.save()

            return HttpResponseRedirect('/')
        # En el caso de que falle el form
        else:
            # Recupera las horas de cierre y apertura en el caso de que falle el form
            opening = form.cleaned_data["opening"]
            closing = form.cleaned_data["closing"]

            # Recupera la provincia del formulario en el caso que falle
            provinceSelected = form.cleaned_data["province"]
            # elimina las provincias duplicadas
            provincesAux = Province.objects.all().exclude(pk=provinceSelected.pk)

    # Si se accede al form vía GET o cualquier otro método
    else:
        # Recupera las horas de cierre y apertura del criador
        opening = association.opening
        closing = association.closing

        # Recupera la provincia de la asociación
        provinceSelected = association.province

        dataForm = {'first_name': association.userAccount.first_name, 'last_name': association.userAccount.last_name,
                    'email': association.userAccount.email, 'centerName': association.centerName,
                    'notes': association.notes, 'province': association.province,
                    'phone': association.phone, 'cif': association.cif, 'photo': association.photo,
                    'opening': association.opening, 'closing': association.closing,
                    'address': association.address, 'private': association.private,
                    'postalCode': association.postalCode}
        form = EditAssociationProfile(dataForm, user=request.user)

    provincesAux = Province.objects.all().exclude(pk=association.province.pk)
    # Datos del modelo (vista)
    data = {
        'form': form,
        'association': association,
        'closing': closing,
        'opening': opening,
        'provincesAux': provincesAux,
        'provinceSelected': provinceSelected,
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


# ELIMINAR LA CUENTA DE UNA ASOCIACION
@login_required(login_url='/login/')
@user_is_association
def delete_association_account(request, pk):
    association = get_object_or_404(Association, pk=pk)
    if request.user.actor.association.pk != association.pk:
        return HttpResponseForbidden()

    if request.method == 'POST':
        User.objects.filter(pk=request.user.pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Se ha borrado su cuenta correctamente')
        return HttpResponseRedirect('/logout')

    return render(request, 'associations/delete_association.html', {'association': association})


"""AMIGOS"""


@login_required(login_url='/login/')
def list_friends(request):
    try:

        # Recuperamos el actor que esta realizando logueado
        actor = request.user.actor

        acceptedStatus = Request.StatusType[1][0]

        # Recupera todas las peticiones que ha enviado el actor y estan aceptadas
        actorFollowers = Request.objects.filter(follower=actor, copy=False, status=acceptedStatus).order_by('follower')

        # Recupera todas las peticiones que ha recibido el actor y estan aceptadas
        actorFolloweds = Request.objects.filter(followed=actor, copy=False, status=acceptedStatus).order_by('followed')

        # Unimos ambas listas
        friend_list_aux = actorFollowers | actorFolloweds

    except Exception as e:

        friend_list_aux = Actor.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(friend_list_aux, 6)

    try:
        friend_list_aux = paginator.page(page)
    except PageNotAnInteger:
        friend_list_aux = paginator.page(1)
    except EmptyPage:
        friend_list_aux = paginator.page(paginator.num_pages)

    data = {
        'friend_list': friend_list_aux,
        'title': 'Listado de amigos',
        # Controlar la vista para los botones
        'isFriends': True,
        'actor': actor,
    }
    return render(request, 'list_friend.html', data)


"""TODOS LOS ACTORES"""


@login_required(login_url='/login/')
def list_actors(request):
    try:
        actor = request.user.actor
        acceptedStatus = Request.StatusType[1][0]

        # Recupera todas las peticiones que ha enviado el actor y estan aceptadas
        requestFollowers = Request.objects.filter(follower=actor, copy=False, status=acceptedStatus)

        # Inicializa la lista que se va a devolver con todos los actores
        actor_list_aux = Actor.objects.all()

        actors = Actor.objects.none()
        actorsFollower = Actor.objects.none()
        actorsFollowed = Actor.objects.none()

        actorsFollowerPending = Actor.objects.none()
        actorsFollowedPending = Actor.objects.none()

        # Recupera los actores de las solicitudes enviadas aceptadas
        for reqFollower in requestFollowers:
            actorsFollower = actorsFollower | Actor.objects.all().filter(pk=reqFollower.followed.pk)

        # Recupera todas las peticiones que ha recibido el actor y estan aceptadas
        requestFolloweds = Request.objects.filter(followed=actor, copy=False, status=acceptedStatus)

        # Recupera todas las peticiones pendientes que ha recibido el actor
        requestReceivedPending = Request.objects.filter(followed=actor, copy=False, status='Pendiente')

        # Recupera los actores con solicitudes pendientes
        for reqRecPending in requestReceivedPending:
            actorsFollowerPending = actorsFollowerPending | Actor.objects.all().filter(pk=reqRecPending.follower.pk)

        # Recupera todas las peticiones pendientes que ha enviado el actor
        requestSentPending = Request.objects.filter(follower=actor, copy=False, status='Pendiente')

        # Recupera los actores con solicitudes pendientes
        for reqSentPending in requestSentPending:
            actorsFollowedPending = actorsFollowedPending | Actor.objects.all().filter(pk=reqSentPending.followed.pk)

        actorsPending = actorsFollowerPending | actorsFollowedPending
        # Elimina duplicados
        actorsPending = actorsPending.distinct()

        # Recupera los actores de las solicitudes recibidas aceptadas
        for reqFollowed in requestFolloweds:
            actorsFollowed = actorsFollowed | Actor.objects.all().filter(pk=reqFollowed.follower.pk)

        # Lista de amigos del actor logueado
        actors = actorsFollower | actorsFollowed

        # Recorremos la lista de amigos y lo quitamos de la lista de actores
        for friend in actors:
            actor_list_aux = actor_list_aux.exclude(pk=friend.pk)

        # Excluye la lista de actores con solicitudes pendientes
        for actPend in actorsPending:
            actor_list_aux = actor_list_aux.exclude(pk=actPend.pk)

        # Excluye el actor logueado
        actor_list_aux = actor_list_aux.exclude(pk=actor.pk).order_by('userAccount')
    except Exception as e:

        actor_list_aux = Actor.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(actor_list_aux, 6)

    try:
        actor_list_aux = paginator.page(page)
    except PageNotAnInteger:
        actor_list_aux = paginator.page(1)
    except EmptyPage:
        actor_list_aux = paginator.page(paginator.num_pages)

    data = {
        'actor_list': actor_list_aux,
        'title': 'Listado de usuarios',
        # Controlar la vista para los botones
        'isAllUsers': True,
        'actorsPending': actorsPending,
    }
    return render(request, 'list_actor.html', data)


"""LISTADO DE ASOCIACIONES"""


def list_associations(request):
    try:
        associacion_list_aux = Association.objects.all().order_by('actor_ptr')

        if hasattr(request.user.actor, 'association'):
            associacion_list_aux = Association.objects.all().exclude(pk=request.user.actor.pk).order_by('actor_ptr')

    except Exception as e:

        associacion_list_aux = Association.objects.all().order_by('actor_ptr')

    page = request.GET.get('page', 1)
    paginator = Paginator(associacion_list_aux, 6)

    try:
        associacion_list_aux = paginator.page(page)
    except PageNotAnInteger:
        associacion_list_aux = paginator.page(1)
    except EmptyPage:
        associacion_list_aux = paginator.page(paginator.num_pages)

    data = {
        'association_list': associacion_list_aux,
        'title': 'Listado de asociaciones',
    }
    return render(request, 'list_association.html', data)


"""LISTADO DE CRIADORES"""


def list_breeders(request):
    try:
        breeder_list_aux = Breeder.objects.all().order_by('actor_ptr')

        if hasattr(request.user.actor, 'breeder'):
            breeder_list_aux = Breeder.objects.all().exclude(pk=request.user.actor.pk).order_by('actor_ptr')

    except Exception as e:

        breeder_list_aux = Breeder.objects.all().order_by('actor_ptr')

    page = request.GET.get('page', 1)
    paginator = Paginator(breeder_list_aux, 6)

    try:
        breeder_list_aux = paginator.page(page)
    except PageNotAnInteger:
        breeder_list_aux = paginator.page(1)
    except EmptyPage:
        breeder_list_aux = paginator.page(paginator.num_pages)

    data = {
        'breeder_list': breeder_list_aux,
        'title': 'Listado de criadores',
    }
    return render(request, 'list_breeder.html', data)


## MOSTRAR PERFIL DEL ACTOR


@login_required(login_url='/login/')
def show_profile(request, pk):
    # Actor del que va a ver el perfil
    recipient = get_object_or_404(Actor, pk=pk)

    # Recupera el actor logueado
    actor = request.user.actor

    # COMPROBUEBA QUE SEA SU AMIGO
    acceptedStatus = Request.StatusType[1][0]

    # Recupera todas las peticiones que ha enviado el actor y estan aceptadas
    requestFollowers = Request.objects.filter(follower=actor, copy=False, status=acceptedStatus)

    actors = Actor.objects.none()
    actorsFollower = Actor.objects.none()
    actorsFollowed = Actor.objects.none()

    # Recupera los actores de las solicitudes enviadas aceptadas
    for reqFollower in requestFollowers:
        actorsFollower = actorsFollower | Actor.objects.all().filter(pk=reqFollower.followed.pk)

    # Recupera todas las peticiones que ha recibido el actor y estan aceptadas
    requestFolloweds = Request.objects.filter(followed=actor, copy=False, status=acceptedStatus)

    # Recupera los actores de las solicitudes recibidas aceptadas
    for reqFollowed in requestFolloweds:
        actorsFollowed = actorsFollowed | Actor.objects.all().filter(pk=reqFollowed.follower.pk)

    # Lista de amigos del actor logueado
    actors = actorsFollower | actorsFollowed

    isFriend = False

    # Recorre la lista de amigos
    for friend in actors:
        # Si el destinatario esta en su lista de amigos
        if friend == recipient:
            isFriend = True

    isRequested = False

    # COMPROBUEBA QUE TENGA UNA SOLICITUD PENDIENTE
    pendingStatus = Request.StatusType[0][0]

    # Recupera todas las peticiones que ha enviado al actor y estan pendientes
    requestPendingFollowers = Request.objects.filter(follower=actor, followed=recipient, copy=False, status=pendingStatus)

    # Recupera todas las peticiones que ha recibido del actor y estan pendientes
    requestPendingFolloweds = Request.objects.filter(follower=recipient, followed=actor, copy=False, status=pendingStatus)

    # Une ambas listas
    allRequestPending = requestPendingFollowers | requestPendingFolloweds

    # Si existe alguna pendiente
    if allRequestPending.count() > 0:
        isRequested = True


    try:
        if recipient.breeder:
            recipient = get_object_or_404(Breeder, pk=pk)
    except:
        try:
            if recipient.association:
                recipient = get_object_or_404(Association, pk=pk)
        except:
                return HttpResponseForbidden()

    data = {
        'actor': recipient,
        'title': 'Perfil del criador',
        'isFriend': isFriend,
        'isRequested': isRequested,
    }
    return render(request, 'show_profile.html', data)
