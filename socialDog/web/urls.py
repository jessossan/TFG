from django.urls import path
from . import views

urlpatterns = [

    # NOTICIAS Y EVENTOS
    path('eventsNews', views.list_eventsNews, name='list_eventsNews'),

]
