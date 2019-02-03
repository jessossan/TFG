from django.urls import path, include
from . import views
import django.contrib.auth.views
from django.conf.urls import url


urlpatterns = [

    # Listado de solicitudes recibidas
    path('listReceived', views.list_requests_received, name='list_requests_received'),

    # Listado de solicitudes enviadas
    path('listSent', views.list_requests_sent, name='list_requests_sent'),

    # Crear solicitud de amistad
    path('create', views.create_request, name='create_request'),

    # Aceptar solicitud
    path('accept/<int:pk>', views.accept_request, name='accept_request'),

    # Rechazar solicitud
    path('reject/<int:pk>', views.reject_request, name='reject_request'),

]
