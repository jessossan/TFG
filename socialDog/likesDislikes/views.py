from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# ACEPTAR PETICIONES
from comments.models import Comment
from dogs.models import Dog
from likesDislikes.models import LikeDislike


@login_required(login_url='/login/')
@csrf_exempt
def like_comment(request, pk):

    # Recupera la solicitud enviada
    comment = get_object_or_404(Comment, pk=pk)

    # Recupera el perro al que ha comentado
    dog = get_object_or_404(Dog, pk=comment.dog.pk)

    # Recupera el actor logueado
    actor = request.user.actor

    # Comprueba que no haya dado ya un like
    checkLikes = LikeDislike.objects.all().filter(like=True, actor=actor, comment=comment).count()
    if (checkLikes > 0):
        return HttpResponseForbidden()

    # Comprueba que no sea su comentario
    if (comment.creator_comment == actor):
        return HttpResponseForbidden()

    # Recupera la request autentica
    like = LikeDislike.objects.create(like=True, actor=actor, comment=comment)

    like.save()

    # Comprueba que si tiene un dislike, se borre y se reste en el atributo dislikes de comentario
    checkDislike = LikeDislike.objects.all().filter(like=False, actor=actor, comment=comment)
    if (checkDislike.count() > 0):
        for dislike in checkDislike:
            dislike.delete()
            comment.dislikes = comment.dislikes - 1
            comment.save()

    # Sumar 1 al atributo likes del comentario
    comment.likes = comment.likes + 1
    comment.save()

    return HttpResponseRedirect('/dogs/profile/' + str(dog.pk))


@login_required(login_url='/login/')
@csrf_exempt
def dislike_comment(request, pk):
    # Recupera la solicitud enviada
    comment = get_object_or_404(Comment, pk=pk)

    # Recupera el perro al que ha comentado
    dog = get_object_or_404(Dog, pk=comment.dog.pk)

    # Recupera el actor logueado
    actor = request.user.actor

    # Comprueba que no haya dado ya un dislike
    checkDislikes = LikeDislike.objects.all().filter(like=False, actor=actor, comment=comment).count()
    if (checkDislikes > 0):
        return HttpResponseForbidden()

    # Comprueba que no sea su comentario
    if (comment.creator_comment == actor):
        return HttpResponseForbidden()

    # Recupera la request autentica
    dislike = LikeDislike.objects.create(like=False, actor=actor, comment=comment)

    dislike.save()

    # Comprueba que si tiene un like, se borre y se reste en el atributo likes de comentario
    checkLike = LikeDislike.objects.all().filter(like=True, actor=actor, comment=comment)
    if (checkLike.count() > 0):
        for like in checkLike:
            like.delete()
            comment.likes = comment.likes - 1
            comment.save()

    # Sumar 1 al atributo dislikes del comentario
    comment.dislikes = comment.dislikes + 1
    comment.save()

    return HttpResponseRedirect('/dogs/profile/' + str(dog.pk))