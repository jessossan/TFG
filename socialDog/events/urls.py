from django.urls import path
from . import views


urlpatterns = [

    # Listados MIS eventos (para criador y asociación)
    path('ownList', views.list_myEvents, name='list_myEvents'),

    # Registro de Evento del criador
    path('breeder/create', views.create_breeder_event, name='create_breeder_event'),

]
