from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from comments.forms import CreateCommentForm
from comments.models import Comment
from dogs.models import Dog


@login_required(login_url='/login/')
def create_comment(request, pk):
    """
	Crear comentario.
	"""
    assert isinstance(request, HttpRequest)

    # Recupera el actor
    actor = request.user.actor

    # Recupera el perro al que va a comentar
    dog = get_object_or_404(Dog, pk=pk)

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = CreateCommentForm(request.POST)
        if (form.is_valid()):

            # Crea el comentario
            text = form.cleaned_data["text"]

            # Creación del comentario
            comment = Comment.objects.create(text=text, creator_comment=actor, dog=dog)

            comment.save()

            return HttpResponseRedirect('/profile/listSent')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = CreateCommentForm()

        # Datos del modelo (vista)

    data = {
        'form': form,
        'title': 'Crea el comentario',
        'year': datetime.now().year,
        # Actor al que se envia el comentario
        'dog': dog,
    }

    return render(request, 'create_comment.html', data)


@login_required(login_url='/login/')
def delete_comment(request, pk):
    actor = request.user.actor
    dog = get_object_or_404(Dog, pk=pk)

    if actor.pk != actor.comment.pk:
        return HttpResponseForbidden()

    # Comprobar que no comente a su perro
    if request.method == 'POST':
        dog.delete()
        return HttpResponseRedirect('/dogs/ownList')

    data = {
        'actor': actor,
        'dog': dog,
    }

    return render(request, 'delete_comment.html', data)
