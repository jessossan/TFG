from django.urls import path
from . import views

urlpatterns = [

    # EVENTOS
    path('events', views.list_events, name='list_events'),

    # NOTICIAS
    path('news', views.list_news, name='list_news'),

]
