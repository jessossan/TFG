from django.urls import path, include
from . import views
import django.contrib.auth.views
from django.conf.urls import url


urlpatterns = [

    # Like
    path('like/<int:pk>', views.like_comment, name='like_comment'),

    # Dislike
    path('dislike/<int:pk>', views.dislike_comment, name='dislike_comment'),

]
