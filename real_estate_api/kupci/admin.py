from django.contrib import admin

from .models import Kupci

# Registruj Admin modul u backendu za Kupce
admin.site.register(Kupci)
