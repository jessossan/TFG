from django.urls import path
from . import views


urlpatterns = [

    # Listado de todos los perros
    path('list', views.list_dogs, name='list_dogs'),

    # Listado de mis perros
    path('ownList', views.list_myDogs, name='list_myDogs'),

    # Registro de Perro
    path('register', views.register_dog, name='register_dog'),

    # Eliminar perro
    path('delete/<int:pk>', views.delete_dog, name='delete_dog'),

    # Editar perro
    path('edit/<int:pk>', views.edit_dog, name='edit_dog'),

]
