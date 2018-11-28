from django.contrib import admin
from MYrequests.models import RequestAdminPanel, Request


# Register your models here.

admin.site.register(Request, RequestAdminPanel)