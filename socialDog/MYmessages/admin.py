from django.contrib import admin
from MYmessages.models import MessageAdminPanel, Message


# Register your models here.

admin.site.register(Message, MessageAdminPanel)