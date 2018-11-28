from django.contrib import admin
from likesDislikes.models import LikeDislikeAdminPanel, LikeDislike


# Register your models here.

admin.site.register(LikeDislike, LikeDislikeAdminPanel)
