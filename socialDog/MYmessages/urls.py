from django.urls import path
from . import views


urlpatterns = [

    # Listado de mensajes recibidos
    path('received', views.list_messages_received, name='list_messages_received'),

    # Responder mensaje recibido
    path('replyReceived/<int:pk>', views.reply_message_received, name='reply_message_received'),

    # Responder mensaje enviado
    path('replySender/<int:pk>', views.reply_message_sent, name='reply_message_sent'),

    # Listado de mensajes enviados
    path('sent', views.list_messages_sent, name='list_messages_sent'),

    # Crear mensaje desde recibidos
    path('createFromReceived', views.create_message_received, name='create_message_received'),

    # Crear mensaje desde enviados
    path('createFromSent', views.create_message_sent, name='create_message_sent'),

    # Eliminar mensaje recibido
    path('deleteReceived/<int:pk>', views.delete_message_received, name='delete_message_received'),

    # Eliminar mensaje enviado
    path('deleteSent/<int:pk>', views.delete_message_sent, name='delete_message_sent'),

]
