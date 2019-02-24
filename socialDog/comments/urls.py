from django.urls import path, include
from . import views
import django.contrib.auth.views
from django.conf.urls import url


urlpatterns = [

    # Crear comentario al perro
    path('create/dog/<int:pk>', views.create_comment, name='create_comment'),

    # Editar comentario al perro
    path('edit/<int:pk>', views.edit_comment, name='edit_comment'),

    # Borrar comentario al perro
    path('delete/<int:pk>', views.delete_comment, name='delete_comment'),

]
