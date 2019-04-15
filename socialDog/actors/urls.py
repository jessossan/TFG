from django.urls import path, include
from . import views
import django.contrib.auth.views
from django.conf.urls import url


urlpatterns = [

    # Edición perfil y pass de Criador
    path('breeder/edit/profile', views.edit_profile_breeder, name='edit_profile_breeder'),
    path('breeder/edit/pass', views.edit_pass_breeder, name='edit_pass_breeder'),

    # Borrado de cuenta de Breeder
    path('', views.delete_breeder_account, name='delete_breeder_account'),
    path('breeder/edit/profile/delete/<int:pk>', views.delete_breeder_account, name='delete_breeder_account'),

    # Edición perfil y pass de Usuario
    path('user/edit/profile', views.edit_profile_customer, name='edit_profile_customer'),
    path('user/edit/pass', views.edit_pass_customer, name='edit_pass_customer'),

    # Borrado de cuenta de Usuario
    path('', views.delete_customer_account, name='delete_customer_account'),
    path('user/edit/profile/delete/<int:pk>', views.delete_customer_account, name='delete_customer_account'),

    # Edición perfil y pass de Asociacion
    path('association/edit/profile', views.edit_profile_association, name='edit_profile_association'),
    path('association/edit/pass', views.edit_pass_association, name='edit_pass_association'),

    # Borrado de cuenta de Asociacion
    path('', views.delete_association_account, name='delete_association_account'),
    path('association/edit/profile/delete/<int:pk>', views.delete_association_account, name='delete_association_account'),

    # Listado de amigos
    path('friends', views.list_friends, name='list_friends'),

    # Listado de usuarios
    path('users', views.list_actors, name='list_actors'),

    # Listado de asociaciones
    path('associations', views.list_associations, name='list_associations'),

    # Listado de criadores
    path('breeders', views.list_breeders, name='list_breeders'),

    # Perfil del actor
    path('profile/<int:pk>', views.show_profile, name='show_profile'),

    # Buscador de actores
    path('search', views.search_actors, name='search_actors'),

]
