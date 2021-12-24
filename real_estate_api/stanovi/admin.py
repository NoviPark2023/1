from django.contrib import admin

from .models import Stanovi


@admin.register(Stanovi)
class StanoviAdmin(admin.ModelAdmin):
    """Registruj Admin modul u backendu za Stanove"""
    inlines = []
