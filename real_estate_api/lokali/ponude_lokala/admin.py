from django.contrib import admin

from .models import PonudeLokala


@admin.register(PonudeLokala)
class PonudeLokaliAdmin(admin.ModelAdmin):
    """Registruj Admin modul u backendu za Ponude Lokala"""
    inlines = []
