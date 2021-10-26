from django.contrib import admin

from .models import Kupci

# Registrovan model Kupci u backend Admin modulu
admin.site.register(Kupci)
