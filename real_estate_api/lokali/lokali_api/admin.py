from django.contrib import admin

from .models import Lokali


@admin.register(Lokali)
class LokaliAdmin(admin.ModelAdmin):
    """Registruj Admin modul u backendu za Lokale"""
    inlines = []
