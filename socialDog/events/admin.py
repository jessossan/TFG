from django.contrib import admin
from events.models import EventAdminPanel, Event

# Register your models here.

admin.site.register(Event, EventAdminPanel)
