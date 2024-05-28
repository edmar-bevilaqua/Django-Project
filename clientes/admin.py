from django.contrib import admin
from .models import Cliente, Pet
# Register your models here.

# Registering the models so they can be found on /admin
admin.site.register(Cliente)
admin.site.register(Pet)
