from django.contrib import admin
from breeds.models import BreedAdminPanel, Breed


# Register your models here.

admin.site.register(Breed, BreedAdminPanel)
