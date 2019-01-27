from django.urls import path
from . import views


urlpatterns = [

    # Listado de mensajes recibidos
    path('received', views.list_messages_received, name='list_messages_received'),

    # Listado de mensajes enviados
    path('sent', views.list_messages_sent, name='list_messages_sent'),

    # Crear mensaje desde recibidos
    path('createFromReceived', views.create_message_received, name='create_message_received'),

    # Crear mensaje desde enviados
    path('createFromSent', views.create_message_sent, name='create_message_sent'),

    # Eliminar mensaje
    #path('delete/<int:pk>', views.delete_message, name='delete_message'),

]
