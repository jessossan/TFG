from django.urls import path, include
from . import views
import django.contrib.auth.views
from django.conf.urls import url


urlpatterns = [

    # Crear comentario al perro
    path('create/dog/<int:pk>', views.create_rate, name='create_rate'),

    # Editar valoración al perro
    path('edit/<int:pk>', views.edit_rate, name='edit_rate'),

    # Borrar valoración al perro
    path('delete/<int:pk>', views.delete_rate, name='delete_rate'),

    # Listar las valoraciones de un perro
    path('list/rates/<int:pk>', views.list_dog_rates, name='list_dog_rates'),

]
