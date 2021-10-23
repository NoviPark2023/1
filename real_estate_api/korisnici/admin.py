from django.contrib import admin

from .models import Korisnici

# Registruj Admin modul u backendu za Korisnike
admin.site.register(Korisnici)
