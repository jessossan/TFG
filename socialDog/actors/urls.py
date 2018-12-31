from django.urls import path, include
from . import views
import django.contrib.auth.views
from django.conf.urls import url


urlpatterns = [

    # Edición perfil y pass de Criador
    path('breeder/edit/profile', views.edit_profile_breeder, name='edit_profile_breeder'),
    path('breeder/edit/pass', views.edit_pass_breeder, name='edit_pass_breeder'),

    # Edición perfil y pass de Usuario
    path('user/edit/profile', views.edit_profile_customer, name='edit_profile_customer'),
    path('user/edit/pass', views.edit_pass_customer, name='edit_pass_customer'),

    # Borrado de cuenta de Usuario
    path('', views.delete_customer_account, name='delete_customer_account'),
    path('user/edit/profile/delete/<int:pk>', views.delete_customer_account, name='delete_customer_account'),

    # Edición perfil y pass de Asociacion
    path('association/edit/profile', views.edit_profile_association, name='edit_profile_association'),
    path('association/edit/pass', views.edit_pass_association, name='edit_pass_association'),

]
