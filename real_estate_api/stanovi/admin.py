from django.contrib import admin

from .models import Stanovi, SlikaStana


# admin.site.register(Stanovi)

class SlikaStanaInline(admin.TabularInline):
    """Reguistruj Tableu slike stana u Adminu -- Inline"""
    model = SlikaStana



@admin.register(Stanovi)
class StanoviAdmin(admin.ModelAdmin):
    inlines = [
        SlikaStanaInline,

    ]
