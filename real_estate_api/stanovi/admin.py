from django.contrib import admin

from .models import Stanovi#, SlikaStana


# admin.site.register(Stanovi)

# class SlikaStanaInline(admin.TabularInline):
#     """Reguistruj Model Slike stana u Adminu backend-u -- Inline"""
#     model = SlikaStana


@admin.register(Stanovi)
class StanoviAdmin(admin.ModelAdmin):
    """Registruj Admin modul u backendu za Stanove sa modelom Slike"""
    inlines = [
        #SlikaStanaInline,
    ]
