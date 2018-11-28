from django.contrib import admin
from comments.models import CommentAdminPanel, Comment

# Register your models here.

admin.site.register(Comment, CommentAdminPanel)
