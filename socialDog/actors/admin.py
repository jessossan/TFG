from django.contrib import admin
from actors.models import Actor, ActorAdminPanel, Administrator, AdministratorAdminPanel, Customer, CustomerAdminPanel
from actors.models import Association, AssociationAdminPanel, Breeder, BreederAdminPanel

# Register your models here.
admin.site.register(Actor, ActorAdminPanel)
admin.site.register(Administrator, AdministratorAdminPanel)
admin.site.register(Customer, CustomerAdminPanel)
admin.site.register(Association, AssociationAdminPanel)
admin.site.register(Breeder, BreederAdminPanel)
