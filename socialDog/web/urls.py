from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_eventsNews, name='list_eventsNews'),

    # NOTICIAS Y EVENTOS
    path('eventsNews', views.list_eventsNews, name='list_eventsNews'),

]
