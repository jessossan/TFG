from django.urls import path
from . import views


urlpatterns = [

    # Listado de mensajes
    #path('', views.list_messages, name='list_messages'),

    # Crear mensaje
    path('create', views.create_message, name='create_message'),

    # Eliminar mensaje
    #path('delete/<int:pk>', views.delete_message, name='delete_message'),

]
