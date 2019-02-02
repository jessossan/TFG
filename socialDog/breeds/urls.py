from django.urls import path, include
from . import views
import django.contrib.auth.views
from django.conf.urls import url


urlpatterns = [

    # Listado de razas
    path('list', views.list_breeds, name='list_breeds'),

]
