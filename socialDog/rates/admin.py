from django.contrib import admin
from rates.models import RateAdminPanel, Rate


# Register your models here.

admin.site.register(Rate, RateAdminPanel)
