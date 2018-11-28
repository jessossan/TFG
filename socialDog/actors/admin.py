from django.contrib import admin
from actors.models import Actor, ActorAdminPanel, Administrator, AdministratorAdminPanel, User, UserAdminPanel
from actors.models import Association, AssociationAdminPanel, Breeder, BreederAdminPanel

# Register your models here.
admin.site.register(Actor, ActorAdminPanel)
admin.site.register(Administrator, AdministratorAdminPanel)
admin.site.register(User, UserAdminPanel)
admin.site.register(Association, AssociationAdminPanel)
admin.site.register(Breeder, BreederAdminPanel)
