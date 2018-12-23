"""socialDogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from datetime import datetime
import web.forms
import web.views
import django.contrib.auth.views
from django.conf.urls.static import static
from socialDog import settings



admin.autodiscover()
handler404 = 'web.views.error404'
handler500 = 'web.views.error500'
handler403 = 'web.views.error403'
handler400 = 'web.views.error400'

urlpatterns = [

    # Administrador
    path('admin/', admin.site.urls),

    # Página de bienvenida
    url(r'^$', web.views.index, name='home'),

    # Sesión
    url(r'^login/$', django.contrib.auth.views.LoginView.as_view(),
        {
            'template_name': 'base/login.html',
            'authentication_form': web.forms.LoginForm,
            'extra_context':
                {
                    'titulo': 'Inicio de sesión',
                    'year': datetime.now().year,
                },
        },
        name='login'),
    url(r'^logout$', django.contrib.auth.views.LogoutView.as_view(),
        {
            'next_page': '/',
        },
        name='logout'),

    # Registro usuario
    url(r'^register/user$', web.views.register_customer, name='registerUser'),

    # Registro asociación
    url(r'^register/association$', web.views.register_association, name='registerAssociation'),

    # Registro criador
    url(r'^register/breeder$', web.views.register_breeder, name='registerBreeder'),

    # Actors
    path('actors/', include('actors.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
