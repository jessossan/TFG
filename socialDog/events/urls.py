from django.urls import path
from . import views


urlpatterns = [

    # Listados MIS eventos (para criador y asociación)
    path('ownList', views.list_myEvents, name='list_myEvents'),

    # Borrar evento (para criador y asociación)
    path('delete/<int:pk>', views.delete_event, name='delete_event'),

    # Editar evento (para criador y asociación)
    path('edit/<int:pk>', views.edit_event, name='edit_event'),

    # Registro de Evento del criador
    path('breeder/create', views.create_breeder_event, name='create_breeder_event'),

]
