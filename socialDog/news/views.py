from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.


# CREACION NOTICIA CRIADOR
from actors.decorators import user_is_breeder, user_is_association
from news.forms import CreateBreederNewsForm, EditNewsForm, CreateAssociationNewsForm
from news.models import News


@login_required(login_url='/login/')
@user_is_breeder
def create_breeder_news(request):
    """
	Registro de la noticia en el sistema.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el criador
    breeder = request.user.actor.breeder

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = CreateBreederNewsForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Crea la noticia
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            photo = form.cleaned_data["photo"]

            # Asigna imagen por defecto si no añade imagen
            if photo == None:
                photo = 'uploads/news-default.png'

            news = News.objects.create(title=title, description=description, photo=photo, breeder=breeder)

            news.save()

            return HttpResponseRedirect('/news/ownList')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = CreateBreederNewsForm()

        # Datos del modelo (vista)

    data = {
        'form': form,
        'title': 'Creación de la noticia',
        'year': datetime.now().year,
    }

    return render(request, 'create_breeder_news.html', data)

@login_required(login_url='/login/')
@user_is_association
def create_association_news(request):
    """
	Registro de la noticia en el sistema.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera la asociación
    association = request.user.actor.association

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = CreateAssociationNewsForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Crea la noticia
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            photo = form.cleaned_data["photo"]

            # Asigna imagen por defecto si no añade imagen
            if photo == None:
                photo = 'uploads/news-default.png'

            news = News.objects.create(title=title, description=description, photo=photo, association=association)

            news.save()

            return HttpResponseRedirect('/news/ownList')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = CreateAssociationNewsForm()

        # Datos del modelo (vista)

    data = {
        'form': form,
        'title': 'Creación de la noticia',
        'year': datetime.now().year,
    }

    return render(request, 'create_association_news.html', data)


# LISTADO DE TODOS MIS NOTICIAS CRIADOR/ASOCIACIÓN
@login_required(login_url='/login/')
def list_myNews(request):
    if hasattr(request.user.actor, 'breeder'):
        # Recupera el criador
        breeder = request.user.actor.breeder
        news_list_aux = News.objects.filter(breeder=breeder)
        ownNews = True

    elif hasattr(request.user.actor, 'association'):
        # Recupera la asociación
        association = request.user.actor.association
        news_list_aux = News.objects.filter(association=association)
        ownNews = True

    else:
        return HttpResponseForbidden()

    page = request.GET.get('page', 1)
    paginator = Paginator(news_list_aux, 6)

    try:
        news_list_aux = paginator.page(page)
    except PageNotAnInteger:
        news_list_aux = paginator.page(1)
    except EmptyPage:
        news_list_aux = paginator.page(paginator.num_pages)

    data = {
        'news_list': news_list_aux,
        'title': 'Listado de mis noticias',
        'ownNews': ownNews,
    }
    return render(request, 'list_news.html', data)

@login_required(login_url='/login/')
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)

    association = None
    breeder = None

    if hasattr(request.user.actor, 'breeder'):
        # Recupera el criador
        breeder = request.user.actor.breeder

        # Comprueba que sea su noticia
        if news.breeder != breeder:
            return HttpResponseForbidden()

    elif hasattr(request.user.actor, 'association'):
        # Recupera la asociación
        association = request.user.actor.association

        # Comprueba que sea su noticia
        if news.association != association:
            return HttpResponseForbidden()

    # Si no es criador o asociacion rechaza
    else:
        return HttpResponseForbidden()

    if request.method == 'POST':
        news.delete()
        return HttpResponseRedirect('/news/ownList')

    # Si el que esta borrando es asociación
    if association is not None:
        data = {
            'association': association,
            'news': news,
        }
    else:
        # Si el que esta borrando es criador
        data = {
            'breeder': breeder,
            'news': news,
        }

    return render(request, 'delete_news.html', data)


@login_required(login_url='/login/')
def edit_news(request, pk):
    """
	Edición de la noticia (para asociacion y criador).
	"""
    assert isinstance(request, HttpRequest)

    news = get_object_or_404(News, pk=pk)
    association = None
    breeder = None

    if hasattr(request.user.actor, 'breeder'):
        # Recupera el criador
        breeder = request.user.actor.breeder

        # Comprueba que sea su noticia
        if news.breeder != breeder:
            return HttpResponseForbidden()

    elif hasattr(request.user.actor, 'association'):
        # Recupera la asociación
        association = request.user.actor.association

        # Comprueba que sea su noticia
        if news.association != association:
            return HttpResponseForbidden()

    # Si no es criador o asociacion rechaza
    else:
        return HttpResponseForbidden()

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditNewsForm(request.POST, request.FILES)
        if (form.is_valid()):
            # Recupera la noticia
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            photo = form.cleaned_data["photo"]

            news.title = title
            news.description = description
            if photo != None:
                news.photo = photo

            news.save()

            return HttpResponseRedirect('/news/ownList')

    # Si se accede al form vía GET o cualquier otro método
    else:
        # Datos del modelo (vista)
        dataForm = {'title': news.title, 'description': news.description, 'photo': news.photo}
        form = EditNewsForm(dataForm)

    data = {
        'form': form,
        'title': 'Edición de la noticia',
        'year': datetime.now().year,
        'news': news,
    }

    return render(request, 'edit_news.html', data)
