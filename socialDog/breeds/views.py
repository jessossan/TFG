from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from breeds.models import Breed


@login_required(login_url='/login/')
def list_breeds(request):
    try:
        breed_list_aux = Breed.objects.all()

    except Exception as e:

        breed_list_aux = Breed.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(breed_list_aux, 6)

    try:
        breed_list_aux = paginator.page(page)
    except PageNotAnInteger:
        breed_list_aux = paginator.page(1)
    except EmptyPage:
        breed_list_aux = paginator.page(paginator.num_pages)

    data = {
        'breed_list': breed_list_aux,
        'title': 'Listado de razas',
    }
    return render(request, 'list_breed.html', data)
