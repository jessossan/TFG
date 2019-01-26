from django.urls import path
from . import views


urlpatterns = [

    # Listados MIS noticias (para criador y asociación)
    path('ownList', views.list_myNews, name='list_myNews'),

    # Borrar una noticia (para criador y asociación)
    path('delete/<int:pk>', views.delete_news, name='delete_news'),

    # Editar noticia (para criador y asociación)
    path('edit/<int:pk>', views.edit_news, name='edit_news'),

    # Registro de noticia del criador
    path('breeder/create', views.create_breeder_news, name='create_breeder_news'),

    # Registro de noticia de la asociacion
    #path('association/create', views.create_association_news, name='create_association_news'),

]
