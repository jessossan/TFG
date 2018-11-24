from django.contrib import admin

# Register your models here.
from socialDog.dogs.models import DogAdminPanel, Dog

admin.site.register(Dog, DogAdminPanel)
