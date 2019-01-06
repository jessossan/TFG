from django.urls import path
from . import views


urlpatterns = [

    # Listado de mis perros

    path('list', views.list_myDogs, name='list_myDogs'),

    # Registro de Perro
    path('register', views.register_dog, name='register_dog'),

]
