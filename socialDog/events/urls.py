from django.urls import path
from . import views


urlpatterns = [

    # Listados MIS eventos (para criador y asociación)
    path('ownList', views.list_myEvents, name='list_myEvents'),

    # Listados MIS eventos POR REALIZAR (para criador y asociación)
    path('ownFutureList', views.list_myFutureEvents, name='list_myFutureEvents'),

    # Listados MIS eventos FINALIZADOS (para criador y asociación)
    path('ownPastList', views.list_myPastEvents, name='list_myPastEvents'),

    # Borrar evento (para criador y asociación)
    path('delete/<int:pk>', views.delete_event, name='delete_event'),

    # Editar evento (para criador y asociación)
    path('edit/<int:pk>', views.edit_event, name='edit_event'),

    # Registro de Evento del criador
    path('breeder/create', views.create_breeder_event, name='create_breeder_event'),

]
