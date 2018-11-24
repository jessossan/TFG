from django.contrib import admin
from dogs.models import Dog, DogAdminPanel

# Register your models here.

admin.site.register(Dog, DogAdminPanel)
