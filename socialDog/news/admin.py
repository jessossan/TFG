from django.contrib import admin
from news.models import NewsAdminPanel, News

# Register your models here.

admin.site.register(News, NewsAdminPanel)
