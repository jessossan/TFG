from django.urls import path, include
from . import views
import django.contrib.auth.views
from django.conf.urls import url


urlpatterns = [

    # Crear comentario al perro
    path('create/dog/<int:pk>', views.create_rate, name='create_rate'),

]
